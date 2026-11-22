"""LLM service powered by google-genai SDK with automated model fallback and cost telemetry."""

import json
import logging
from typing import Optional, Tuple
from google import genai
from google.genai import types
from google.genai.errors import APIError

from app.config import get_settings
from app.schemas import LLMAnalysisOutput, TechnicalSeoAudit

logger = logging.getLogger(__name__)


class LLMServiceError(Exception):
    """Base exception for LLM operations."""
    pass


class LLMTimeoutError(LLMServiceError):
    """Raised when upstream LLM API request times out."""
    pass


class LLMAuthenticationError(LLMServiceError):
    """Raised when GEMINI_API_KEY is missing or invalid."""
    pass


class LLMUpstreamError(LLMServiceError):
    """Raised when upstream LLM service encounters unrecoverable failure."""
    pass


class LLMGenerationResult:
    """Encapsulates structured LLM payload with actual execution telemetry."""

    def __init__(
        self,
        analysis_data: LLMAnalysisOutput,
        model_used: str,
        input_tokens: int,
        output_tokens: int,
        estimated_cost_usd: float,
    ):
        self.analysis_data = analysis_data
        self.model_used = model_used
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.estimated_cost_usd = estimated_cost_usd


class LLMService:
    """Asynchronous LLM service orchestrating Gemini 2.5 Flash and Gemini 2.5 Flash-Lite."""

    def __init__(self, api_key: Optional[str] = None):
        self.settings = get_settings()
        self.api_key = api_key or self.settings.GEMINI_API_KEY
        self.client: Optional[genai.Client] = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    def _calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate exact monetary cost based on published rates per million tokens."""
        if "lite" in model_name.lower():
            input_rate = self.settings.GEMINI_2_5_FLASH_LITE_INPUT_COST_PER_M
            output_rate = self.settings.GEMINI_2_5_FLASH_LITE_OUTPUT_COST_PER_M
        else:
            input_rate = self.settings.GEMINI_2_5_FLASH_INPUT_COST_PER_M
            output_rate = self.settings.GEMINI_2_5_FLASH_OUTPUT_COST_PER_M

        cost = (input_tokens * input_rate + output_tokens * output_rate) / 1_000_000.0
        return round(cost, 6)

    def _build_prompt(
        self,
        website_url: str,
        distilled_content: str,
        seo_audit: TechnicalSeoAudit,
    ) -> str:
        """Construct prompt containing technical SEO facts and website content."""
        audit_context = (
            f"- Extracted Title: {seo_audit.title or 'None'}\n"
            f"- Title Length: {seo_audit.title_char_count} chars\n"
            f"- Extracted Meta Description: {seo_audit.meta_description or 'None'}\n"
            f"- Meta Description Length: {seo_audit.meta_description_char_count} chars\n"
            f"- H1 Tags ({seo_audit.h1_count}): {', '.join(seo_audit.h1_tags) if seo_audit.h1_tags else 'None'}\n"
            f"- H2 Tags: {seo_audit.h2_count}, H3 Tags: {seo_audit.h3_count}\n"
            f"- Images Audit: {seo_audit.total_images} total, {seo_audit.images_missing_alt} missing alt\n"
            f"- Internal Navigation Anchor Labels: {', '.join(seo_audit.internal_nav_links[:10]) if seo_audit.internal_nav_links else 'None'}\n"
            f"- Schema Types Detected: {', '.join(seo_audit.schema_types_detected) if seo_audit.schema_types_detected else 'None'}\n"
        )

        return (
            f"You are a top-1% Chief Marketing Officer and Technical SEO Specialist. "
            f"Perform an exhaustive strategic and SEO analysis of the website at URL: {website_url}.\n\n"
            f"--- DETERMINISTIC TECHNICAL SEO FACTS ---\n"
            f"{audit_context}\n"
            f"--- EXTRACTED HIGH-SIGNAL WEBSITE CONTENT ---\n"
            f"{distilled_content}\n\n"
            f"--- MANDATORY ANALYSIS SPECIFICATIONS ---\n"
            f"1. BRAND:\n"
            f"   - name, category, and executive summary.\n"
            f"2. COMPETITOR ANALYSIS:\n"
            f"   - brand_overview, main_products_and_services, your_brand_strengths, and opportunities.\n"
            f"   - competitors: Minimum 3 realistic market competitors. Each competitor MUST include name, main_service, target_market, strengths, weaknesses_or_gaps, and source_note explicitly stating 'AI-inferred market positioning based on industry benchmark data.'\n"
            f"3. TARGET SEARCH QUERIES:\n"
            f"   - Exactly 5 high-intent queries covering: 'Google Search', 'Facebook', 'Instagram', 'LinkedIn', and 'X (Twitter)'.\n"
            f"   - Each item includes query, platforms (list), intent, business_relevance, and target_audience.\n"
            f"   - STRICT RULE: Never invent numeric search volumes, CPCs, or ranking positions.\n"
            f"4. SEO IMPROVEMENTS:\n"
            f"   - primary_keyword, secondary_keywords, long_tail_keywords, business_keywords.\n"
            f"   - recommended_title (50-60 chars) with title_rationale.\n"
            f"   - meta_description (140-160 chars).\n"
            f"   - supporting_content: list of typed items with type ('Service Landing Page', 'Industry Page', 'FAQ', 'Blog Topic', 'Location Page'), title, and description.\n"
            f"5. TOP SERVICES:\n"
            f"   - Up to 5 services with service_name, description, target_industry, target_customer, main_benefit, and extraction_source ('Explicitly stated on website' vs 'Inferred from website context').\n"
            f"6. TARGET AUDIENCE:\n"
            f"   - primary_audience, secondary_audience, industries, business_types, customer_profiles, geographical_focus, customer_needs, customer_interests, and recommended_marketing_segments (segment_name, business_type, requirement).\n\n"
            f"Ensure strict conformity to the requested JSON schema."
        )

    async def generate_analysis(
        self,
        website_url: str,
        distilled_content: str,
        seo_audit: TechnicalSeoAudit,
    ) -> LLMGenerationResult:
        """Execute structured generation using primary model with automatic fallback to secondary model."""
        if not self.client:
            if not self.api_key:
                raise LLMAuthenticationError(
                    "GEMINI_API_KEY environment variable is not configured. "
                    "Please provide a valid Google Gemini API key."
                )
            self.client = genai.Client(api_key=self.api_key)

        prompt = self._build_prompt(website_url, distilled_content, seo_audit)

        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=LLMAnalysisOutput,
            temperature=0.2,
        )

        models_to_try = [
            (self.settings.PRIMARY_MODEL, "primary"),
            (self.settings.FALLBACK_MODEL, "fallback"),
        ]

        last_exception: Optional[Exception] = None

        for model_name, tier in models_to_try:
            try:
                logger.info("Initiating LLM generation with %s model '%s'...", tier, model_name)
                response = await self.client.aio.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config,
                )

                # Extract token usage
                input_tokens = 0
                output_tokens = 0
                if hasattr(response, "usage_metadata") and response.usage_metadata:
                    input_tokens = getattr(response.usage_metadata, "prompt_token_count", 0) or 0
                    output_tokens = getattr(response.usage_metadata, "candidates_token_count", 0) or 0

                estimated_cost = self._calculate_cost(model_name, input_tokens, output_tokens)

                # Parse Pydantic output
                analysis_output: LLMAnalysisOutput
                if hasattr(response, "parsed") and isinstance(response.parsed, LLMAnalysisOutput):
                    analysis_output = response.parsed
                elif hasattr(response, "text") and response.text:
                    analysis_output = LLMAnalysisOutput.model_validate_json(response.text)
                else:
                    raise LLMUpstreamError(f"Model {model_name} returned an empty or unparseable response.")

                logger.info(
                    "LLM generation successful using '%s' (Prompt Tokens: %d, Output Tokens: %d, Cost: $%.6f)",
                    model_name,
                    input_tokens,
                    output_tokens,
                    estimated_cost,
                )

                return LLMGenerationResult(
                    analysis_data=analysis_output,
                    model_used=model_name,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    estimated_cost_usd=estimated_cost,
                )

            except APIError as api_err:
                logger.warning(
                    "%s model '%s' encountered APIError: %s. Attempting fallback if available...",
                    tier.capitalize(),
                    model_name,
                    api_err,
                )
                last_exception = api_err
            except Exception as exc:
                logger.warning(
                    "%s model '%s' failed with error: %s (%s). Attempting fallback if available...",
                    tier.capitalize(),
                    model_name,
                    exc,
                    type(exc).__name__,
                )
                last_exception = exc

        # All models failed
        logger.error("All LLM models in hierarchy failed to generate analysis. Last error: %s", last_exception)
        raise LLMUpstreamError(
            f"Upstream AI generation failed across both primary and fallback models: {last_exception}"
        ) from last_exception
