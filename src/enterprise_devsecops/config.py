"""Application configuration.

Settings are loaded from environment variables (optionally via a `.env`
file) using pydantic-settings. See `.env.example` for the full list of
supported variables.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the enterprise-devsecops platform."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="EDSEC_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="enterprise-devsecops", description="Service name.")
    environment: str = Field(
        default="development",
        description="Deployment environment: development, staging, or production.",
    )
    log_level: str = Field(default="INFO", description="Python logging level.")
    log_json: bool = Field(default=False, description="Emit logs as JSON instead of plain text.")

    host: str = Field(default="0.0.0.0", description="Bind host for the HTTP service.")
    port: int = Field(default=8080, description="Bind port for the HTTP service.")

    policy_path: str = Field(
        default="policies/org-policy.yaml",
        description="Path to the organization security policy file.",
    )
    default_fail_on: str = Field(
        default="HIGH",
        description="Minimum finding severity that fails a deployment gate by default.",
    )

    scan_report_bucket: str = Field(
        default="",
        description="Object storage bucket where scan reports/findings are archived.",
    )
    scanner_timeout_seconds: int = Field(
        default=900,
        description="Maximum time allotted to a single scanner invocation.",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached `Settings` instance."""
    return Settings()
