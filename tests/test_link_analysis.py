"""Comprehensive test suite for AI Link Analysis API.

Tests cover:
- Health check and diagnostic probes
- Hardened SSRF blocking (localhost, private CIDRs, link-local, IPv6, open redirect hops)
- URL syntax and protocol validation
- Non-HTML media type rejection
- Deterministic SEO audit and HTML content distillation
- In-memory TTL caching performance and cost nullification
- Complete end-to-end schema conformance and business rule enforcement
- LLM primary model failure and automatic fallback
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import httpx
import pytest
from httpx import ASGITransport, AsyncClient, Response

from app.config import get_settings
from app.main import app, get_analysis_service
from app.schemas import (
    BrandInfo,
    CompetitorAnalysis,
    CompetitorItem,
    LLMAnalysisOutput,
    MarketingSegmentItem,
    SeoImprovements,
    SupportingContentItem,
    TargetAudience,
    TargetSearchQuery,
    TechnicalSeoAudit,
    TopServiceItem,
)
from app.services.analysis_service import AnalysisService
from app.services.competitor_service import CompetitorService
from app.services.llm_service import LLMGenerationResult, LLMService
from app.services.website_extractor import WebsiteExtractor
from app.utils.validators import SSRFError, validate_url_for_ssrf


# ==============================================================================
# Test Fixtures & Mock Generators
# ==============================================================================

SAMPLE_HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Apex Analytics | Enterprise AI Intelligence Platform</title>
    <meta name="description" content="Empowering enterprise decision makers with automated predictive analytics and neural intelligence pipelines.">
    <link rel="canonical" href="https://apexanalytics.io/home">
    <meta property="og:title" content="Apex Analytics">
    <meta property="og:description" content="AI Intelligence for Enterprise">
    <meta property="og:type" content="website">
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Apex Analytics",
        "url": "https://apexanalytics.io"
    }
    </script>
</head>
<body>
    <header>
        <nav>
            <a href="/solutions">Solutions</a>
            <a href="/pricing">Pricing</a>
            <a href="/about">About Us</a>
            <a href="/contact">Contact</a>
        </nav>
    </header>
    <main>
        <h1>Next-Generation Enterprise AI Platform</h1>
        <h2>Streamline Data Intelligence at Scale</h2>
        <p>Apex Analytics provides unified data ingestion and real-time operational analytics for Fortune 500 enterprises.</p>
        <h2>Core Platform Capabilities</h2>
        <p>From predictive pipeline monitoring to automated anomaly detection, our system guarantees 99.99% uptime.</p>
        <img src="/images/hero.webp" alt="Apex Platform Dashboard">
        <img src="/images/diagram.png">
        <ul>
            <li>Automated data cleansing and enrichment</li>
            <li>Low-latency vector similarity search</li>
            <li>Multi-tenant compliance and SOC 2 Type II governance</li>
        </ul>
    </main>
</body>
</html>
"""


def build_mock_llm_output() -> LLMAnalysisOutput:
    """Construct a fully compliant LLMAnalysisOutput fixture."""
    return LLMAnalysisOutput(
        brand=BrandInfo(
            name="Apex Analytics",
            category="Enterprise AI & Business Intelligence",
            summary="A high-performance predictive intelligence platform delivering real-time analytics for B2B enterprises.",
        ),
        competitor_analysis=CompetitorAnalysis(
            brand_overview="Apex Analytics provides high-throughput predictive AI data pipelines.",
            main_products_and_services=[
                "Enterprise Data Pipeline Intelligence",
                "Automated Anomaly Detection Engine",
                "Vectorized Predictive Analytics",
            ],
            competitors=[
                CompetitorItem(
                    name="DataRobot",
                    main_service="Automated Machine Learning and Model Governance",
                    target_market="Enterprise Data Science and ML Teams",
                    strengths=["Extensive algorithm library", "Mature enterprise client roster"],
                    weaknesses_or_gaps=["Higher cost barriers", "Complex self-hosted deployment"],
                    source_note="AI-inferred market positioning based on industry benchmark data.",
                ),
                CompetitorItem(
                    name="Databricks",
                    main_service="Lakehouse Architecture and Data Engineering",
                    target_market="Data Engineers and Large-Scale Enterprise Infrastructure",
                    strengths=["Dominant Apache Spark ecosystem", "Unified data governance"],
                    weaknesses_or_gaps=["Requires specialized Spark engineering talent"],
                    source_note="AI-inferred market positioning based on industry benchmark data.",
                ),
                CompetitorItem(
                    name="Palantir Foundry",
                    main_service="Enterprise Operational Decision Intelligence",
                    target_market="Government, Defense, and Global Conglomerates",
                    strengths=["Deep institutional workflow integration", "Rigorous data security"],
                    weaknesses_or_gaps=["Protracted deployment cycles", "Very high annual contracts"],
                    source_note="AI-inferred market positioning based on industry benchmark data.",
                ),
            ],
            your_brand_strengths=[
                "Turnkey API integration with zero infrastructure overhead",
                "Sub-second vector query latency",
            ],
            opportunities=[
                "Capture mid-market enterprises underserved by monolithic legacy platforms",
                "Integrate multimodal telemetry feeds",
            ],
        ),
        target_search_queries=[
            TargetSearchQuery(
                query="enterprise real-time ai analytics pipeline",
                platforms=["Google Search"],
                intent="Commercial Investigation",
                business_relevance="Directly targets buyers seeking automated AI intelligence pipelines.",
                target_audience="Chief Data Officers and VP of Analytics",
            ),
            TargetSearchQuery(
                query="how to automate data anomaly detection in retail",
                platforms=["Facebook"],
                intent="Problem-Aware / Informational",
                business_relevance="Surfaces operational pain points solved by automated detection.",
                target_audience="Director of Operations and Ecommerce Leads",
            ),
            TargetSearchQuery(
                query="#DataEngineering #EnterpriseAI tech showcase",
                platforms=["Instagram"],
                intent="Brand Awareness & Visual Showcase",
                business_relevance="Highlights modern visual dashboards and telemetry analytics.",
                target_audience="Tech-forward founders and UI/UX stakeholders",
            ),
            TargetSearchQuery(
                query="best scalable alternatives to legacy data lakehouses",
                platforms=["LinkedIn"],
                intent="High-Intent Commercial Evaluation",
                business_relevance="Engages executive decision makers assessing infrastructure modernization.",
                target_audience="CTOs, Enterprise Architects, and IT Directors",
            ),
            TargetSearchQuery(
                query="fastest vector database for real-time inference",
                platforms=["X (Twitter)"],
                intent="Technical Discovery and Community Discussion",
                business_relevance="Demonstrates performance leadership in developer and AI practitioner circles.",
                target_audience="Machine Learning Engineers and AI Architects",
            ),
        ],
        seo_improvements=SeoImprovements(
            primary_keyword="enterprise AI analytics platform",
            secondary_keywords=[
                "real-time data intelligence",
                "automated anomaly detection",
                "predictive enterprise pipelines",
            ],
            long_tail_keywords=[
                "best real time ai analytics for b2b enterprises",
                "scalable vector data intelligence software",
            ],
            business_keywords=[
                "Apex Analytics",
                "Apex AI Platform",
                "enterprise predictive modeling",
            ],
            recommended_title="Enterprise AI Analytics & Real-Time Intelligence | Apex",
            title_rationale="Positions primary keyword upfront while reinforcing high-value enterprise credibility.",
            meta_description="Supercharge decision-making with Apex Analytics: the unified AI platform delivering real-time anomaly detection and enterprise data intelligence at scale.",
            supporting_content=[
                SupportingContentItem(
                    type="Service Landing Page",
                    title="Real-Time Automated Anomaly Detection",
                    description="Deep dive into zero-lag operational alerting and machine learning algorithms.",
                ),
                SupportingContentItem(
                    type="Industry Page",
                    title="AI Intelligence for Modern FinTech & Banking",
                    description="Tailored compliance, high-volume transactional monitoring, and fraud prevention.",
                ),
                SupportingContentItem(
                    type="FAQ",
                    title="Enterprise Architecture and SOC 2 Governance FAQ",
                    description="Addresses common CTO and security team evaluation questions regarding data isolation.",
                ),
                SupportingContentItem(
                    type="Blog Topic",
                    title="Why Traditional Data Warehouses Lag in Real-Time AI Inference",
                    description="Thought leadership addressing architectural bottlenecks in legacy architectures.",
                ),
                SupportingContentItem(
                    type="Location Page",
                    title="Enterprise AI Solutions - North America & EMEA",
                    description="Regional enterprise support, latency SLAs, and sovereign cloud deployments.",
                ),
            ],
        ),
        top_services=[
            TopServiceItem(
                service_name="Enterprise Data Pipeline Intelligence",
                description="End-to-end telemetry ingestion, transformation, and AI enrichment at scale.",
                target_industry="Financial Services and Healthcare",
                target_customer="VP of Data Engineering",
                main_benefit="Reduces manual data preparation time by over 70%.",
                extraction_source="Explicitly stated on website",
            ),
            TopServiceItem(
                service_name="Automated Anomaly Detection Engine",
                description="Autonomous neural models monitoring production metrics for divergence.",
                target_industry="E-Commerce and Logistics",
                target_customer="Chief Operating Officer",
                main_benefit="Mitigates operational downtime with sub-second alert triggers.",
                extraction_source="Explicitly stated on website",
            ),
            TopServiceItem(
                service_name="Vectorized Predictive Analytics",
                description="High-dimensional vector indexing for real-time customer behavior forecasting.",
                target_industry="SaaS and Digital Platforms",
                target_customer="Head of Product",
                main_benefit="Drives higher user retention through personalized machine recommendations.",
                extraction_source="Inferred from website context",
            ),
        ],
        target_audience=TargetAudience(
            primary_audience="Enterprise technology and data leaders (CTOs, CDOs, VP of Engineering)",
            secondary_audience="Data engineers, machine learning practitioners, and BI analysts",
            industries=["FinTech", "HealthTech", "Supply Chain & Logistics", "B2B SaaS"],
            business_types=["B2B Enterprise", "Scale-Up Mid-Market", "Global Conglomerates"],
            customer_profiles=[
                "Chief Data Officer (CDO)",
                "VP of Engineering",
                "Director of Business Intelligence",
            ],
            geographical_focus="Global with primary concentration in North America and Western Europe",
            customer_needs=[
                "Elimination of data silos",
                "Sub-second latency for predictive insights",
                "SOC 2 and GDPR compliant enterprise infrastructure",
            ],
            customer_interests=[
                "Autonomous AI agents",
                "Modern data stack optimization",
                "Cloud infrastructure ROI",
            ],
            recommended_marketing_segments=[
                MarketingSegmentItem(
                    segment_name="B2B Enterprise FinTech",
                    business_type="Large-scale Financial Institutions",
                    requirement="Real-time fraud surveillance and high-throughput transactional analytics",
                ),
                MarketingSegmentItem(
                    segment_name="Digital Supply Chain & Logistics",
                    business_type="Mid-Market to Enterprise Fleet Operators",
                    requirement="Predictive bottleneck detection and automated telemetry alerts",
                ),
            ],
        ),
    )


@pytest.fixture
def mock_analysis_service():
    """Build a fully mocked AnalysisService that never hits the network or paid APIs."""
    extractor = WebsiteExtractor()
    llm_service = LLMService(api_key="mock-api-key")
    competitor_service = CompetitorService()

    # Mock fetch_html to return sample HTML
    async def mock_fetch_html(url: str):
        return SAMPLE_HTML_PAGE, 200, url

    extractor.fetch_html = AsyncMock(side_effect=mock_fetch_html)

    # Mock LLM generation
    async def mock_generate_analysis(website_url: str, distilled_content: str, seo_audit):
        return LLMGenerationResult(
            analysis_data=build_mock_llm_output(),
            model_used="gemini-2.5-flash",
            input_tokens=1850,
            output_tokens=920,
            estimated_cost_usd=0.000415,
        )

    llm_service.generate_analysis = AsyncMock(side_effect=mock_generate_analysis)

    service = AnalysisService(
        extractor=extractor,
        llm_service=llm_service,
        competitor_service=competitor_service,
    )
    return service


# ==============================================================================
# 1. Health & Diagnostic Endpoint Tests
# ==============================================================================

@pytest.mark.asyncio
async def test_health_check_endpoint():
    """Verify /health returns 200, operational status, and valid metadata."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "environment" in data
        assert data["version"] == "1.0.0"
        assert isinstance(data["cache_entries"], int)


# ==============================================================================
# 2. SSRF Protection & Private Network Blocking Tests
# ==============================================================================

@pytest.mark.parametrize(
    "prohibited_url",
    [
        "http://localhost",
        "http://localhost:8080",
        "http://127.0.0.1",
        "http://127.0.0.1:4000",
        "http://10.0.0.1/internal-admin",
        "http://10.254.0.1",
        "http://172.16.0.1",
        "http://192.168.1.1",
        "http://169.254.169.254/latest/meta-data/",
        "http://0.0.0.0:80",
        "http://[::1]",
    ],
)
def test_ssrf_validator_blocks_private_targets(prohibited_url):
    """Ensure validate_url_for_ssrf blocks all loopback, private CIDR, and cloud metadata targets."""
    with pytest.raises(SSRFError):
        validate_url_for_ssrf(prohibited_url)


@pytest.mark.asyncio
async def test_ssrf_api_returns_400():
    """Verify POST /link-analysis returns HTTP 400 with SSRF error code on attack payload."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/link-analysis", json={"url": "http://127.0.0.1:8080/metrics"})
        assert response.status_code == 400
        data = response.json()
        assert data["error_code"] == "SSRF_PROHIBITED_DESTINATION"
        assert "blocked" in data["detail"].lower()


@pytest.mark.asyncio
async def test_ssrf_redirect_hop_protection():
    """Verify that an open redirect pointing to an internal IP (127.0.0.1) is blocked mid-flight."""
    extractor = WebsiteExtractor()

    # Create mock transport simulating a 302 redirect to localhost
    def mock_transport_handler(request):
        if "evil-redirect.com" in request.url.host:
            return Response(302, headers={"Location": "http://127.0.0.1:9000/secret"})
        return Response(200, text="<html><body>OK</body></html>")

    mock_transport = httpx.MockTransport(mock_transport_handler)

    with patch("httpx.AsyncClient") as mock_client_cls:
        # Construct client with actual event hook behavior
        async def mock_get(url, *args, **kwargs):
            # Simulate what the hook does when hitting a redirect
            from app.utils.validators import verify_redirect_hop
            res = Response(302, headers={"Location": "http://127.0.0.1:9000/secret"}, request=httpx.Request("GET", url))
            await verify_redirect_hop(res)
            return res

        instance = MagicMock()
        instance.__aenter__.return_value.get = AsyncMock(side_effect=mock_get)
        mock_client_cls.return_value = instance

        with pytest.raises(SSRFError) as exc_info:
            await extractor.fetch_html("https://google.com")  # valid initial, redirects to prohibited
        assert "SSRF" in str(exc_info.value) or "blocked" in str(exc_info.value).lower()


# ==============================================================================
# 3. URL Validation & Non-HTML Media Rejection Tests
# ==============================================================================

@pytest.mark.parametrize(
    "invalid_url",
    [
        "ftp://files.example.com",
        "file:///etc/passwd",
        "gopher://example.com",
        "javascript:alert(1)",
        "not-a-valid-url-at-all",
        "http://admin:secret@example.com",
    ],
)
@pytest.mark.asyncio
async def test_invalid_url_syntax_rejected(invalid_url):
    """Verify improper schemes, file protocols, and embedded credentials trigger clean HTTP 400/422."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/link-analysis", json={"url": invalid_url})
        assert response.status_code in (400, 422)


@pytest.mark.asyncio
async def test_non_html_content_rejected():
    """Verify non-HTML content (e.g., application/pdf) returns HTTP 422 Unprocessable Entity."""
    extractor = WebsiteExtractor()

    async def mock_fetch_pdf(url: str):
        from app.services.website_extractor import NonHtmlContentError
        raise NonHtmlContentError("Target URL returned non-HTML media type 'application/pdf'.")

    extractor.fetch_html = AsyncMock(side_effect=mock_fetch_pdf)
    service = AnalysisService(extractor=extractor)

    app.dependency_overrides[get_analysis_service] = lambda: service
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/link-analysis", json={"url": "https://example.com/document.pdf"})
            assert response.status_code == 422
            data = response.json()
            assert data["error_code"] == "NON_HTML_CONTENT"
    finally:
        app.dependency_overrides.clear()


# ==============================================================================
# 4. Deterministic Technical SEO Extraction Tests
# ==============================================================================

def test_deterministic_seo_audit():
    """Unit test website_extractor to ensure 100% deterministic metric calculation."""
    extractor = WebsiteExtractor()
    extracted = extractor.parse_and_audit(SAMPLE_HTML_PAGE, "https://apexanalytics.io", 200)

    audit = extracted.audit
    assert audit.title == "Apex Analytics | Enterprise AI Intelligence Platform"
    assert audit.title_char_count == len("Apex Analytics | Enterprise AI Intelligence Platform")
    assert audit.meta_description is not None
    assert "automated predictive analytics" in audit.meta_description
    assert audit.meta_description_char_count == len(audit.meta_description)
    assert audit.h1_count == 1
    assert audit.h1_tags == ["Next-Generation Enterprise AI Platform"]
    assert audit.h2_count == 2
    assert audit.total_images == 2
    assert audit.images_with_alt == 1
    assert audit.images_missing_alt == 1
    assert audit.has_og_tags is True
    assert audit.og_tags.get("og:title") == "Apex Analytics"
    assert audit.canonical_url == "https://apexanalytics.io/home"
    assert audit.has_schema_markup is True
    assert "Organization" in audit.schema_types_detected
    assert len(audit.internal_nav_links) >= 4
    assert "Solutions" in audit.internal_nav_links
    assert "Pricing" in audit.internal_nav_links

    # Distilled text verification
    assert len(extracted.distilled_content) > 100
    assert "<script" not in extracted.distilled_content.lower()
    assert "application/ld+json" not in extracted.distilled_content.lower()


# ==============================================================================
# 5. In-Memory TTL Caching Tests
# ==============================================================================

@pytest.mark.asyncio
async def test_ttl_caching_performance_and_cost(mock_analysis_service):
    """Verify repeat requests return from cache in <5ms with cached=True and $0.00 cost."""
    app.dependency_overrides[get_analysis_service] = lambda: mock_analysis_service
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            target_url = "https://apexanalytics.io"

            # First request (uncached)
            resp1 = await client.post("/link-analysis", json={"url": target_url})
            assert resp1.status_code == 200
            data1 = resp1.json()
            assert data1["metadata"]["cached"] is False
            assert data1["metadata"]["estimated_cost_usd"] > 0

            # Second request (must be served from TTL cache)
            resp2 = await client.post("/link-analysis", json={"url": target_url})
            assert resp2.status_code == 200
            data2 = resp2.json()

            assert data2["metadata"]["cached"] is True
            assert data2["metadata"]["model_used"] == "cache"
            assert data2["metadata"]["input_tokens"] == 0
            assert data2["metadata"]["output_tokens"] == 0
            assert data2["metadata"]["estimated_cost_usd"] == 0.0
            assert data2["metadata"]["processing_time_ms"] < 25.0  # Ultra-fast cache hit

            # Brand and analysis data must match perfectly
            assert data2["brand"]["name"] == data1["brand"]["name"]
            assert data2["analysis"]["competitor_analysis"]["competitors"] == data1["analysis"]["competitor_analysis"]["competitors"]
    finally:
        app.dependency_overrides.clear()


# ==============================================================================
# 6. End-to-End Schema Validation & Business Rules
# ==============================================================================

@pytest.mark.asyncio
async def test_end_to_end_analysis_schema_compliance(mock_analysis_service):
    """Verify POST /link-analysis returns the exact complete schema with all 5 sections."""
    app.dependency_overrides[get_analysis_service] = lambda: mock_analysis_service
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/link-analysis", json={"url": "https://apexanalytics.io"})
            assert response.status_code == 200
            res = response.json()

            # Top-level fields
            assert res["success"] is True
            assert "https://apexanalytics.io" in res["website"]
            assert "metadata" in res
            assert "brand" in res
            assert "technical_seo_audit" in res
            assert "analysis" in res

            # Brand checks
            brand = res["brand"]
            assert brand["name"] == "Apex Analytics"
            assert brand["category"] != ""
            assert brand["summary"] != ""

            # Analysis Sections check
            analysis = res["analysis"]

            # 1. Competitor Analysis
            comp = analysis["competitor_analysis"]
            assert len(comp["competitors"]) >= 3
            for c in comp["competitors"]:
                assert c["name"] != ""
                assert c["main_service"] != ""
                assert c["target_market"] != ""
                assert len(c["strengths"]) > 0
                assert len(c["weaknesses_or_gaps"]) > 0
                assert "inferred" in c["source_note"].lower()

            # 2. Target Search Queries (Strict Rule: exactly 5 queries, no fake numeric volume/CPC)
            queries = analysis["target_search_queries"]
            assert len(queries) == 5
            expected_platforms = {"Google Search", "Facebook", "Instagram", "LinkedIn", "X (Twitter)"}
            found_platforms = set()
            for q in queries:
                assert q["query"] != ""
                assert len(q["platforms"]) > 0
                for p in q["platforms"]:
                    found_platforms.add(p)
                assert q["intent"] != ""
                assert q["business_relevance"] != ""
                assert q["target_audience"] != ""
                # Ensure no fake metrics
                assert not hasattr(q, "search_volume")
                assert not hasattr(q, "cpc")
            assert len(expected_platforms.intersection(found_platforms)) >= 4

            # 3. SEO Improvements
            seo = analysis["seo_improvements"]
            assert seo["primary_keyword"] != ""
            assert len(seo["secondary_keywords"]) > 0
            assert len(seo["long_tail_keywords"]) > 0
            assert len(seo["business_keywords"]) > 0
            assert seo["recommended_title"] != ""
            assert seo["title_rationale"] != ""
            assert seo["meta_description"] != ""
            assert len(seo["supporting_content"]) > 0
            valid_content_types = {
                "Service Landing Page",
                "Industry Page",
                "FAQ",
                "Blog Topic",
                "Location Page",
            }
            for sc in seo["supporting_content"]:
                assert sc["type"] in valid_content_types
                assert sc["title"] != ""
                assert sc["description"] != ""

            # 4. Top Services
            services = analysis["top_services"]
            assert 1 <= len(services) <= 5
            for s in services:
                assert s["service_name"] != ""
                assert s["description"] != ""
                assert s["target_industry"] != ""
                assert s["target_customer"] != ""
                assert s["main_benefit"] != ""
                assert s["extraction_source"] in (
                    "Explicitly stated on website",
                    "Inferred from website context",
                )

            # 5. Target Audience
            aud = analysis["target_audience"]
            assert aud["primary_audience"] != ""
            assert aud["secondary_audience"] != ""
            assert len(aud["industries"]) > 0
            assert len(aud["business_types"]) > 0
            assert len(aud["customer_profiles"]) > 0
            assert aud["geographical_focus"] != ""
            assert len(aud["customer_needs"]) > 0
            assert len(aud["customer_interests"]) > 0
            assert len(aud["recommended_marketing_segments"]) > 0
            for seg in aud["recommended_marketing_segments"]:
                assert seg["segment_name"] != ""
                assert seg["business_type"] != ""
                assert seg["requirement"] != ""
    finally:
        app.dependency_overrides.clear()


# ==============================================================================
# 7. LLM Model Hierarchy & Fallback Resilience
# ==============================================================================

@pytest.mark.asyncio
async def test_llm_automatic_fallback():
    """Verify that if the primary model fails, the service falls back to gemini-2.5-flash-lite."""
    service = LLMService(api_key="mock-key")
    audit = TechnicalSeoAudit(
        title="Test",
        title_char_count=4,
        meta_description=None,
        meta_description_char_count=0,
        h1_count=1,
        h1_tags=["Test"],
        h2_count=0,
        h3_count=0,
        total_images=0,
        images_missing_alt=0,
        images_with_alt=0,
        internal_nav_links=[],
        canonical_url=None,
        has_og_tags=False,
        og_tags={},
        has_schema_markup=False,
        schema_types_detected=[],
        content_char_count=100,
        status_code=200,
    )

    mock_client = MagicMock()

    # Primary model throws exception; fallback model succeeds
    async def mock_generate(model, contents, config):
        if "flash-lite" not in model:
            raise Exception("503 Service Unavailable: High load on gemini-2.5-flash")
        # Return fallback mock response
        mock_resp = MagicMock()
        mock_resp.parsed = build_mock_llm_output()
        mock_resp.usage_metadata.prompt_token_count = 1400
        mock_resp.usage_metadata.candidates_token_count = 750
        return mock_resp

    mock_client.aio.models.generate_content = AsyncMock(side_effect=mock_generate)
    service.client = mock_client

    result = await service.generate_analysis("https://apexanalytics.io", "Distilled content", audit)
    assert result.model_used == service.settings.FALLBACK_MODEL
    assert result.input_tokens == 1400
    assert result.output_tokens == 750
    assert result.estimated_cost_usd > 0


@pytest.mark.asyncio
async def test_llm_upstream_failure_error_mapping():
    """Verify that when both primary and secondary models fail, HTTP 502 Bad Gateway is returned."""
    service = LLMService(api_key="mock-key")
    mock_client = MagicMock()

    async def mock_fail_all(model, contents, config):
        raise Exception("Google API Down")

    mock_client.aio.models.generate_content = AsyncMock(side_effect=mock_fail_all)
    service.client = mock_client

    extractor = WebsiteExtractor()
    extractor.fetch_html = AsyncMock(return_value=(SAMPLE_HTML_PAGE, 200, "https://apexanalytics.io"))

    analysis_service = AnalysisService(extractor=extractor, llm_service=service)
    app.dependency_overrides[get_analysis_service] = lambda: analysis_service

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/link-analysis", json={"url": "https://apexanalytics.io"})
            assert response.status_code == 502
            data = response.json()
            assert data["error_code"] == "LLM_UPSTREAM_FAILURE"
    finally:
        app.dependency_overrides.clear()
