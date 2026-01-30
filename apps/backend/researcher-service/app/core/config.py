"""
Configuration settings for Researcher Service.
Loads settings from environment variables with fallbacks.
"""
import os
from typing import Optional
from pydantic import Field
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
    app_name: str = Field(default="Researcher Portal Service")
    debug: bool = Field(default=False)
    
    # Database - use same connection as identity-service
    database_url: str = Field(
        default="postgresql://postgres.zmdkpplpycidyponszkh:Vaibhav2154@aws-1-ap-south-1.pooler.supabase.com:5432/postgres",
        description="PostgreSQL connection string"
    )
    
    # Security
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        min_length=32,
        description="JWT secret key"
    )
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60, ge=1)
    refresh_token_expire_days: int = Field(default=7, ge=1)
    
    # CORS
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:3001,http://localhost:5173",
        description="Comma-separated list of allowed CORS origins"
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # API
    api_v1_prefix: str = Field(default="/api/v1")
    
    # External Services (for consent validation)
    consent_service_url: str = Field(
        default="http://localhost:8001",
        description="Base URL for Consent Service"
    )
    policy_engine_url: str = Field(
        default="http://localhost:8003",
        description="Base URL for Policy Engine"
    )


settings = Settings()
