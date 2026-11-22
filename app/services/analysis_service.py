"""Central orchestration and in-memory TTL caching service for link analysis."""

import asyncio
import copy
import logging
import time
from typing import Dict, Optional, Tuple

from app.config import get_settings
from app.schemas import (
    AnalysisMetadata,
    AnalysisSections,
    LinkAnalysisResponse,
)
from app.services.competitor_service import CompetitorService
from app.services.llm_service import LLMService
from app.services.website_extractor import WebsiteExtractor
from app.utils.validators import normalize_url, validate_url_for_ssrf

logger = logging.getLogger(__name__)


class CacheEntry:
    """Represents a cached response payload paired with an epoch timestamp."""

    def __init__(self, response: LinkAnalysisResponse, timestamp: float):
        self.response = response
        self.timestamp = timestamp


class InMemoryTTLCache:
    """Thread-safe and async-safe in-memory cache enforcing Time-To-Live (TTL)."""

    def __init__(self, ttl_seconds: int = 3600):
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[LinkAnalysisResponse]:
        """Retrieve cached response if within TTL window, otherwise purge expired entry."""
        async with self._lock:
            entry = self._cache.get(key)
            if not entry:
                return None

            now = time.time()
            if now - entry.timestamp > self.ttl_seconds:
                del self._cache[key]
                return None

            # Return a clone to prevent external mutation
            return copy.deepcopy(entry.response)

    async def set(self, key: str, value: LinkAnalysisResponse) -> None:
        """Store response in cache associated with current timestamp."""
        async with self._lock:
            self._cache[key] = CacheEntry(
                response=copy.deepcopy(value),
                timestamp=time.time(),
            )

    async def size(self) -> int:
        """Return count of active valid entries."""
        async with self._lock:
            now = time.time()
            # Clean expired items
            keys_to_remove = [k for k, v in self._cache.items() if now - v.timestamp > self.ttl_seconds]
            for k in keys_to_remove:
                del self._cache[k]
            return len(self._cache)

    async def clear(self) -> None:
        """Purge all cached entries."""
        async with self._lock:
            self._cache.clear()


class AnalysisService:
    """End-to-end pipeline orchestrator for AI-powered website link analysis."""

    def __init__(
        self,
        extractor: Optional[WebsiteExtractor] = None,
        llm_service: Optional[LLMService] = None,
        competitor_service: Optional[CompetitorService] = None,
    ):
        self.settings = get_settings()
        self.extractor = extractor or WebsiteExtractor()
        self.llm_service = llm_service or LLMService()
        self.competitor_service = competitor_service or CompetitorService()
        self.cache = InMemoryTTLCache(ttl_seconds=self.settings.CACHE_TTL_SECONDS)

    async def analyze_url(self, raw_url: str) -> LinkAnalysisResponse:
        """Execute end-to-end link analysis with SSRF security, deterministic SEO audit, and LLM reasoning.

        1. Validates and normalizes URL.
        2. Inspects TTL in-memory cache (<5ms cache hit path).
        3. Scrapes HTML safely and performs deterministic technical SEO audit.
        4. Synthesizes brand, competitor, search query, SEO, and audience intelligence.
        5. Caches and returns production response.
        """
        start_time = time.perf_counter()

        # Step 1: SSRF validation & URL canonical normalization
        validated_url = validate_url_for_ssrf(raw_url)
        normalized_key = normalize_url(validated_url)

        # Step 2: Check TTL cache
        cached_response = await self.cache.get(normalized_key)
        if cached_response:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            logger.info("Cache hit for %s in %.2f ms", normalized_key, elapsed_ms)
            cached_response.metadata.cached = True
            cached_response.metadata.processing_time_ms = round(elapsed_ms, 2)
            cached_response.metadata.model_used = "cache"
            cached_response.metadata.input_tokens = 0
            cached_response.metadata.output_tokens = 0
            cached_response.metadata.estimated_cost_usd = 0.0
            return cached_response

        # Step 3: Fetch HTML & perform deterministic SEO audit
        html_text, status_code, final_url = await self.extractor.fetch_html(validated_url)
        extracted = self.extractor.parse_and_audit(html_text, final_url, status_code)

        # Step 4: Execute structured LLM intelligence generation
        llm_result = await self.llm_service.generate_analysis(
            website_url=final_url,
            distilled_content=extracted.distilled_content,
            seo_audit=extracted.audit,
        )

        # Step 5: Competitor intelligence refinement and business rule validation
        refined_competitor_analysis = self.competitor_service.validate_and_refine(
            competitor_analysis=llm_result.analysis_data.competitor_analysis,
            brand_category=llm_result.analysis_data.brand.category,
        )

        # Step 6: Assemble complete analysis sections
        analysis_sections = AnalysisSections(
            competitor_analysis=refined_competitor_analysis,
            target_search_queries=llm_result.analysis_data.target_search_queries,
            seo_improvements=llm_result.analysis_data.seo_improvements,
            top_services=llm_result.analysis_data.top_services,
            target_audience=llm_result.analysis_data.target_audience,
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metadata = AnalysisMetadata(
            model_used=llm_result.model_used,
            cached=False,
            processing_time_ms=round(elapsed_ms, 2),
            input_tokens=llm_result.input_tokens,
            output_tokens=llm_result.output_tokens,
            estimated_cost_usd=llm_result.estimated_cost_usd,
        )

        response = LinkAnalysisResponse(
            success=True,
            website=normalized_key,
            metadata=metadata,
            brand=llm_result.analysis_data.brand,
            technical_seo_audit=extracted.audit,
            analysis=analysis_sections,
        )

        # Step 7: Populate TTL cache
        await self.cache.set(normalized_key, response)

        logger.info(
            "Successfully completed link analysis for %s in %.2f ms (Cost: $%.6f)",
            normalized_key,
            elapsed_ms,
            llm_result.estimated_cost_usd,
        )

        return response
