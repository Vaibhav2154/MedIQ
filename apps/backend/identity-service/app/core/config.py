"""
Configuration settings for Identity Service.
Loads settings from environment variables.
"""
import os
from typing import Optional
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = Field(default="Identity Service")
    debug: bool = Field(default=False)
    
    # Database
    database_url: PostgresDsn = Field(
        ...,
        description="PostgreSQL connection string"
    )
    
    # Database Pool Settings
    db_pool_size: int = Field(default=5, ge=1, le=20)
    db_max_overflow: int = Field(default=10, ge=0, le=20)
    db_pool_timeout: int = Field(default=30, ge=1)
    db_pool_recycle: int = Field(default=3600, ge=60)
    
    # Security
    secret_key: str = Field(..., min_length=32)
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30, ge=1)
    
    # CORS
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        description="Comma-separated list of allowed CORS origins"
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # API
    api_v1_prefix: str = Field(default="/api/v1")

    # External Services
    consent_ingestion_url: str = Field(
        default="http://localhost:8002",
        description="Base URL for Consent Ingestion Service"
    )
    consent_intelligence_url: str = Field(
        default="http://localhost:8001",
        description="Base URL for Consent Intelligence Service"
    )


settings = Settings()
