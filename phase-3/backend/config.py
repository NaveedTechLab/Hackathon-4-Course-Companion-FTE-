from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Claude API Settings
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY", "")
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-3-sonnet-20240229")

    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://localhost/course_companion")

    # Application Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Feature Flags
    ENABLE_PREMIUM_FEATURES: bool = os.getenv("ENABLE_PREMIUM_FEATURES", "true").lower() == "true"
    ZERO_BACKEND_LLM_DEFAULT: bool = True  # Always true for Phase 1/3 deterministic features

    # Token Usage Limits
    TOKEN_USAGE_LIMIT_PER_USER_PER_DAY: int = int(os.getenv("TOKEN_USAGE_LIMIT_PER_USER_PER_DAY", "100000"))

    # Premium Pricing
    PREMIUM_TIER_COST_PER_THOUSAND_TOKENS: float = float(os.getenv("PREMIUM_TIER_COST_PER_THOUSAND_TOKENS", "0.015"))

    # Cloud Storage (R2)
    CLOUDFLARE_ACCOUNT_ID: str = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
    CLOUDFLARE_R2_ACCESS_KEY_ID: str = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID", "")
    CLOUDFLARE_R2_SECRET_ACCESS_KEY: str = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY", "")
    CLOUDFLARE_R2_BUCKET_NAME: str = os.getenv("CLOUDFLARE_R2_BUCKET_NAME", "")

    # Allowed Origins for CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://localhost:3000",
        "https://localhost:3001"
    ]

    class Config:
        env_file = ".env"

settings = Settings()