"""Pydantic data schemas and contract definitions for AI Link Analysis."""

from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field, HttpUrl, field_validator


# ==============================================================================
# Request Schemas
# ==============================================================================

class LinkAnalysisRequest(BaseModel):
    """Incoming request payload for website link analysis."""

    url: str = Field(
        ...,
        description="Target website URL to analyze (must be http or https)",
        examples=["https://example.com"],
    )

    @field_validator("url")
    @classmethod
    def validate_url_syntax(cls, v: str) -> str:
        """Preliminary sanity check on URL formatting."""
        v = v.strip()
        if not v:
            raise ValueError("URL cannot be empty.")
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("URL must specify http:// or https:// protocol scheme.")
        return v


# ==============================================================================
# Telemetry & Metadata Schemas
# ==============================================================================

class AnalysisMetadata(BaseModel):
    """Runtime telemetry and computational cost metrics."""

    model_used: str = Field(
        ...,
        description="LLM model identifier utilized for generating intelligence",
        examples=["gemini-2.5-flash", "cache"],
    )
    cached: bool = Field(
        ...,
        description="Indicates whether the response was served from in-memory TTL cache",
    )
    processing_time_ms: float = Field(
        ...,
        description="End-to-end processing latency in milliseconds",
    )
    input_tokens: int = Field(
        ...,
        description="Prompt tokens consumed by the LLM generation",
    )
    output_tokens: int = Field(
        ...,
        description="Completion tokens produced by the LLM generation",
    )
    estimated_cost_usd: float = Field(
        ...,
        description="Estimated monetary cost in USD based on official token pricing",
    )


# ==============================================================================
# Brand & Technical SEO Schemas
# ==============================================================================

class BrandInfo(BaseModel):
    """Synthesized brand identity and categorical domain."""

    name: str = Field(..., description="Entity or brand commercial name")
    category: str = Field(..., description="Primary industry or business classification")
    summary: str = Field(..., description="High-level executive overview of brand operations")


class TechnicalSeoAudit(BaseModel):
    """Deterministically extracted technical SEO metrics from the target HTML."""

    title: Optional[str] = Field(None, description="Extracted HTML document title")
    title_char_count: int = Field(..., description="Character count of the title tag")
    meta_description: Optional[str] = Field(None, description="Extracted meta description")
    meta_description_char_count: int = Field(
        ...,
        description="Character count of the meta description",
    )
    h1_count: int = Field(..., description="Total count of <h1> tags detected")
    h1_tags: List[str] = Field(
        default_factory=list,
        description="Extracted text of all <h1> tags",
    )
    h2_count: int = Field(..., description="Total count of <h2> tags detected")
    h3_count: int = Field(..., description="Total count of <h3> tags detected")
    total_images: int = Field(..., description="Total <img> tags found on the page")
    images_missing_alt: int = Field(
        ...,
        description="Count of <img> tags missing descriptive alt text",
    )
    images_with_alt: int = Field(..., description="Count of <img> tags with valid alt text")
    internal_nav_links: List[str] = Field(
        default_factory=list,
        description="Extracted anchor text labels from internal navigation menus",
    )
    canonical_url: Optional[str] = Field(
        None,
        description="Canonical URL declared in <link rel='canonical'>",
    )
    has_og_tags: bool = Field(
        ...,
        description="Whether OpenGraph metadata tags were detected",
    )
    og_tags: Dict[str, str] = Field(
        default_factory=dict,
        description="Map of extracted OpenGraph properties and values",
    )
    has_schema_markup: bool = Field(
        ...,
        description="Whether JSON-LD structured schema markup was present",
    )
    schema_types_detected: List[str] = Field(
        default_factory=list,
        description="List of detected Schema.org @type entities",
    )
    content_char_count: int = Field(
        ...,
        description="Character count of the distilled high-signal text payload",
    )
    status_code: int = Field(
        ...,
        description="HTTP response status code returned by the target host",
    )


# ==============================================================================
# Intelligence Section 1: Competitor Analysis
# ==============================================================================

class CompetitorItem(BaseModel):
    """Individual competitor profile and market comparison."""

    name: str = Field(..., description="Competitor organization or brand name")
    main_service: str = Field(..., description="Core competing product or service offering")
    target_market: str = Field(..., description="Primary geographic or customer segment served")
    strengths: List[str] = Field(..., description="Key competitive advantages of competitor")
    weaknesses_or_gaps: List[str] = Field(
        ...,
        description="Observed vulnerabilities or unaddressed market gaps",
    )
    source_note: str = Field(
        ...,
        description="Explicit note clarifying AI-inferred market positioning and competitive context",
    )


class CompetitorAnalysis(BaseModel):
    """Competitive landscape overview and strategic benchmarking."""

    brand_overview: str = Field(
        ...,
        description="Executive synopsis of the analyzed brand's market posture",
    )
    main_products_and_services: List[str] = Field(
        ...,
        description="Core products and solutions marketed by the brand",
    )
    competitors: List[CompetitorItem] = Field(
        ...,
        min_length=3,
        description="Minimum 3 market competitors with strengths, gaps, and AI-inferred source notes",
    )
    your_brand_strengths: List[str] = Field(
        ...,
        description="Distinctive strategic strengths of the analyzed brand",
    )
    opportunities: List[str] = Field(
        ...,
        description="Strategic market openings and competitive differentiation opportunities",
    )


# ==============================================================================
# Intelligence Section 2: Target Search Queries
# ==============================================================================

class TargetSearchQuery(BaseModel):
    """Multi-platform search query recommendation without synthetic metrics."""

    query: str = Field(..., description="High-intent search query or hashtag/topic phrase")
    platforms: List[str] = Field(
        ...,
        description="Applicable discovery platforms (Google Search, Facebook, Instagram, LinkedIn, X (Twitter))",
    )
    intent: str = Field(
        ...,
        description="Search intent classification (e.g., Commercial, Transactional, Informational, Problem-Aware)",
    )
    business_relevance: str = Field(
        ...,
        description="Strategic justification of how this query aligns with core business offerings",
    )
    target_audience: str = Field(
        ...,
        description="Specific buyer persona or customer group driving this search phrase",
    )


# ==============================================================================
# Intelligence Section 3: SEO Improvements
# ==============================================================================

SupportingContentType = Literal[
    "Service Landing Page",
    "Industry Page",
    "FAQ",
    "Blog Topic",
    "Location Page",
]


class SupportingContentItem(BaseModel):
    """Recommended architectural content expansion item."""

    type: SupportingContentType = Field(
        ...,
        description="Class of supporting digital content asset",
    )
    title: str = Field(..., description="Proposed page headline or article title")
    description: str = Field(
        ...,
        description="Content outline and commercial intent alignment",
    )


class SeoImprovements(BaseModel):
    """On-page and semantic search optimization recommendations."""

    primary_keyword: str = Field(..., description="Core high-priority commercial keyword")
    secondary_keywords: List[str] = Field(
        ...,
        description="Secondary thematic keywords supporting core relevance",
    )
    long_tail_keywords: List[str] = Field(
        ...,
        description="High-specificity long-tail phrases capturing conversion intent",
    )
    business_keywords: List[str] = Field(
        ...,
        description="Commercial terms reflecting specific products, services, or brand value props",
    )
    recommended_title: str = Field(
        ...,
        description="Optimized HTML <title> tag recommendation (50-60 characters)",
    )
    title_rationale: str = Field(
        ...,
        description="Strategic rationale behind keyword order and CTR psychology",
    )
    meta_description: str = Field(
        ...,
        description="Optimized meta description recommendation (140-160 characters)",
    )
    supporting_content: List[SupportingContentItem] = Field(
        ...,
        description="Targeted content assets to build topical authority across typed page classes",
    )


# ==============================================================================
# Intelligence Section 4: Top Services
# ==============================================================================

ExtractionSourceType = Literal[
    "Explicitly stated on website",
    "Inferred from website context",
]


class TopServiceItem(BaseModel):
    """Extracted or inferred core service offering."""

    service_name: str = Field(..., description="Commercial name or description of service")
    description: str = Field(..., description="Summary of service deliverables and scope")
    target_industry: str = Field(..., description="Specific vertical or industry sector served")
    target_customer: str = Field(..., description="Target buyer persona or stakeholder title")
    main_benefit: str = Field(..., description="Primary ROI or value proposition delivered")
    extraction_source: ExtractionSourceType = Field(
        ...,
        description="Clear attribution whether offering is directly stated or contextually inferred",
    )


# ==============================================================================
# Intelligence Section 5: Target Audience
# ==============================================================================

class MarketingSegmentItem(BaseModel):
    """Specific actionable market segment."""

    segment_name: str = Field(..., description="Descriptive title of customer segment")
    business_type: str = Field(
        ...,
        description="Organizational structure (e.g., B2B Enterprise, Mid-Market D2C, Boutique Agency)",
    )
    requirement: str = Field(
        ...,
        description="Core operational requirement or trigger prompting engagement",
    )


class TargetAudience(BaseModel):
    """Demographic, firmographic, and behavioral audience breakdown."""

    primary_audience: str = Field(..., description="Primary ICP (Ideal Customer Profile)")
    secondary_audience: str = Field(..., description="Secondary influencer or user demographic")
    industries: List[str] = Field(..., description="Target industries and vertical sectors")
    business_types: List[str] = Field(..., description="Business structures and scale categories")
    customer_profiles: List[str] = Field(
        ...,
        description="Key decision maker personas and stakeholder roles",
    )
    geographical_focus: str = Field(
        ...,
        description="Primary geographic territories and regional market focus",
    )
    customer_needs: List[str] = Field(
        ...,
        description="Underlying business pain points and functional requirements",
    )
    customer_interests: List[str] = Field(
        ...,
        description="Aspirational interests and strategic priorities of buyers",
    )
    recommended_marketing_segments: List[MarketingSegmentItem] = Field(
        ...,
        description="Actionable customer segments with specific organizational needs",
    )


# ==============================================================================
# Top-Level Aggregated Schemas
# ==============================================================================

class AnalysisSections(BaseModel):
    """The 5 foundational intelligence sections generated from link analysis."""

    competitor_analysis: CompetitorAnalysis = Field(
        ...,
        description="Section 1: Competitive landscape and strategic gap analysis",
    )
    target_search_queries: List[TargetSearchQuery] = Field(
        ...,
        min_length=5,
        max_length=5,
        description="Section 2: Exactly 5 multi-platform high-intent search queries without fake metrics",
    )
    seo_improvements: SeoImprovements = Field(
        ...,
        description="Section 3: On-page keywords, title/meta recommendations, and supporting content",
    )
    top_services: List[TopServiceItem] = Field(
        ...,
        max_length=5,
        description="Section 4: Up to 5 key services with explicit vs inferred attribution",
    )
    target_audience: TargetAudience = Field(
        ...,
        description="Section 5: Audience personas, geographic focus, and marketing segments",
    )


class LLMAnalysisOutput(BaseModel):
    """Direct structured output schema requested from the Gemini model."""

    brand: BrandInfo
    competitor_analysis: CompetitorAnalysis
    target_search_queries: List[TargetSearchQuery] = Field(min_length=5, max_length=5)
    seo_improvements: SeoImprovements
    top_services: List[TopServiceItem] = Field(max_length=5)
    target_audience: TargetAudience


class LinkAnalysisResponse(BaseModel):
    """Complete production response schema for POST /link-analysis."""

    success: bool = Field(default=True, description="Execution success indicator")
    website: str = Field(..., description="Normalized target website URL analyzed")
    metadata: AnalysisMetadata = Field(..., description="Runtime performance and cost telemetry")
    brand: BrandInfo = Field(..., description="Brand entity profile and classification")
    technical_seo_audit: TechnicalSeoAudit = Field(
        ...,
        description="Deterministic on-page technical SEO audit results",
    )
    analysis: AnalysisSections = Field(
        ...,
        description="Comprehensive 5-part AI-generated market and SEO intelligence",
    )


class HealthResponse(BaseModel):
    """Service health and diagnostic status."""

    status: str = Field(default="ok", description="Operational status")
    environment: str = Field(..., description="Active server environment")
    version: str = Field(..., description="API semantic version")
    cache_entries: int = Field(..., description="Current count of active in-memory cached URLs")


class ErrorResponse(BaseModel):
    """Standardized error response payload."""

    detail: str = Field(..., description="Descriptive error explanation")
    error_code: str = Field(..., description="Machine-readable error classification code")
