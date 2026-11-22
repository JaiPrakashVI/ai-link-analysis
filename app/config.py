"""Application configuration management via Pydantic Settings."""

from functools import lru_cache
from typing import Literal
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Production settings schema supporting environment variables and .env overrides."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Core API secrets and identifiers
    GEMINI_API_KEY: str = Field(
        default="",
        description="Google Gemini API key for LLM structured generations",
    )

    # Server Bind Configuration
    APP_HOST: str = Field(default="0.0.0.0", description="Host binding IP")
    APP_PORT: int = Field(
        default=4000,
        validation_alias=AliasChoices("APP_PORT", "PORT"),
        description="Server port (accepts APP_PORT or standard Cloud PORT)",
    )
    ENVIRONMENT: Literal["development", "staging", "production", "test"] = Field(
        default="production",
        description="Deployment runtime environment",
    )

    # LLM Model Hierarchy & Fallback
    PRIMARY_MODEL: str = Field(
        default="gemini-3.1-flash-lite",
        description="Primary model for high-signal structured link analysis",
    )
    FALLBACK_MODEL: str = Field(
        default="gemini-3.5-flash-lite",
        description="Resilience fallback model in case of primary model unavailability",
    )

    # In-Memory TTL Cache Configuration
    CACHE_TTL_SECONDS: int = Field(
        default=3600,
        description="Cache validity window in seconds (default 1 hour)",
    )

    # Web Scraping & Ingestion Guardrails
    REQUEST_TIMEOUT_SECONDS: float = Field(
        default=15.0,
        description="HTTP network request timeout in seconds",
    )
    MAX_CONTENT_CHARS: int = Field(
        default=15000,
        description="Maximum characters of distilled text payload sent to LLM context",
    )
    MAX_REDIRECTS: int = Field(
        default=5,
        description="Maximum redirect hops before aborting HTTP connection",
    )
    MAX_RETRIES: int = Field(
        default=2,
        description="Retry attempts for transient external failures",
    )

    # Published LLM Pricing (USD per 1,000,000 tokens)
    GEMINI_2_5_FLASH_INPUT_COST_PER_M: float = 0.075
    GEMINI_2_5_FLASH_OUTPUT_COST_PER_M: float = 0.30
    GEMINI_2_5_FLASH_LITE_INPUT_COST_PER_M: float = 0.0375
    GEMINI_2_5_FLASH_LITE_OUTPUT_COST_PER_M: float = 0.15


@lru_cache()
def get_settings() -> Settings:
    """Retrieve cached singleton instance of Settings."""
    return Settings()
