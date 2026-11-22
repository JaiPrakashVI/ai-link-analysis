"""Main FastAPI application entry point for AI-Powered Website Link Analysis."""

import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.config import get_settings
from app.schemas import (
    ErrorResponse,
    HealthResponse,
    LinkAnalysisRequest,
    LinkAnalysisResponse,
)
from app.services.analysis_service import AnalysisService
from app.services.llm_service import (
    LLMAuthenticationError,
    LLMServiceError,
    LLMTimeoutError,
    LLMUpstreamError,
)
from app.services.website_extractor import (
    NonHtmlContentError,
    WebsiteExtractionError,
    WebsiteHTTPError,
    WebsiteTimeoutError,
)
from app.utils.validators import InvalidURLError, SSRFError

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ai_link_analysis")

settings = get_settings()

# Global singleton analysis service instance
analysis_service_instance = AnalysisService()


def get_analysis_service() -> AnalysisService:
    """Dependency provider for AnalysisService."""
    return analysis_service_instance


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown procedures."""
    logger.info("Initializing AI Link Analysis service (Environment: %s)...", settings.ENVIRONMENT)
    yield
    logger.info("Shutting down AI Link Analysis service. Purging cache...")
    await analysis_service_instance.cache.clear()


app = FastAPI(
    title="AI Link Analysis API",
    description=(
        "Production-grade, asynchronous website link intelligence API. "
        "Performs hardened SSRF validation, deterministic on-page technical SEO auditing, "
        "and multi-dimensional competitive benchmarking using Google Gemini models."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Enable Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================================================
# Custom Exception Handlers for Strict HTTP Error Mapping
# ==============================================================================

@app.exception_handler(SSRFError)
async def ssrf_exception_handler(request: Request, exc: SSRFError):
    logger.warning("SSRF violation prevented from %s: %s", request.client.host if request.client else "unknown", exc)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc), "error_code": "SSRF_PROHIBITED_DESTINATION"},
    )


@app.exception_handler(InvalidURLError)
async def invalid_url_exception_handler(request: Request, exc: InvalidURLError):
    logger.info("Invalid URL rejected: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc), "error_code": "INVALID_URL"},
    )


@app.exception_handler(NonHtmlContentError)
async def non_html_exception_handler(request: Request, exc: NonHtmlContentError):
    logger.info("Non-HTML content rejected: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc), "error_code": "NON_HTML_CONTENT"},
    )


@app.exception_handler(WebsiteTimeoutError)
async def website_timeout_exception_handler(request: Request, exc: WebsiteTimeoutError):
    logger.warning("Upstream website timeout: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content={"detail": str(exc), "error_code": "TARGET_WEBSITE_TIMEOUT"},
    )


@app.exception_handler(LLMTimeoutError)
async def llm_timeout_exception_handler(request: Request, exc: LLMTimeoutError):
    logger.error("LLM inference timeout: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content={"detail": str(exc), "error_code": "LLM_INFERENCE_TIMEOUT"},
    )


@app.exception_handler(LLMAuthenticationError)
async def llm_auth_exception_handler(request: Request, exc: LLMAuthenticationError):
    logger.error("LLM authentication failure: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"detail": str(exc), "error_code": "LLM_AUTHENTICATION_ERROR"},
    )


@app.exception_handler(LLMUpstreamError)
async def llm_upstream_exception_handler(request: Request, exc: LLMUpstreamError):
    logger.error("LLM upstream error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"detail": str(exc), "error_code": "LLM_UPSTREAM_FAILURE"},
    )


@app.exception_handler(WebsiteHTTPError)
async def website_http_exception_handler(request: Request, exc: WebsiteHTTPError):
    logger.warning("Target website HTTP error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"detail": str(exc), "error_code": "TARGET_WEBSITE_ERROR"},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = [f"{e['loc'][-1]}: {e['msg']}" for e in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "; ".join(error_messages),
            "error_code": "VALIDATION_ERROR",
        },
    )


# ==============================================================================
# API Endpoints
# ==============================================================================

@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check and service diagnostics",
    tags=["Diagnostics"],
)
async def health_check(
    service: AnalysisService = Depends(get_analysis_service),
) -> HealthResponse:
    """Verify service readiness, environment tier, and active cache utilization."""
    cache_count = await service.cache.size()
    return HealthResponse(
        status="ok",
        environment=settings.ENVIRONMENT,
        version="1.0.0",
        cache_entries=cache_count,
    )


@app.post(
    "/link-analysis",
    response_model=LinkAnalysisResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid URL format or SSRF violation"},
        422: {"model": ErrorResponse, "description": "Non-HTML content or schema validation error"},
        502: {"model": ErrorResponse, "description": "Upstream LLM or website network failure"},
        504: {"model": ErrorResponse, "description": "Gateway connection timeout"},
    },
    summary="Analyze website link for SEO, competitor, and brand intelligence",
    tags=["Analysis"],
)
async def perform_link_analysis(
    payload: LinkAnalysisRequest,
    service: AnalysisService = Depends(get_analysis_service),
) -> LinkAnalysisResponse:
    """Perform end-to-end website link analysis.

    - **SSRF Validation**: Ensures URL does not resolve to private, loopback, or cloud metadata IPs.
    - **High-Signal Extraction**: Extracts headings, metadata, schema markup, and strips boilerplate.
    - **Technical SEO Audit**: Computes deterministic metrics (tag counts, missing alt tags, etc.).
    - **AI Intelligence**: Synthesizes competitors, 5-platform search queries, keywords, services, and audience personas.
    - **TTL Caching**: Caches results in memory for 1 hour to provide sub-5ms responses on repeat requests.
    """
    return await service.analyze_url(payload.url)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=(settings.ENVIRONMENT == "development"),
    )
