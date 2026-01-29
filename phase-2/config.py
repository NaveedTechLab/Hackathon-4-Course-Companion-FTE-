from pydantic_settings import BaseSettings
from typing import Optional, List
import os
from dotenv import load_dotenv

# Load .env file first
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_PORT: int = int(os.getenv("API_PORT", "8001"))
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "true").lower() == "true"
    ALLOWED_ORIGINS: List[str] = ["*"]
    # OpenRouter API Settings (Primary)
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    llm_model: str = os.getenv("LLM_MODEL", "openai/gpt-3.5-turbo")

    # OpenAI API Settings (Alternative)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    # Claude API Settings (kept for backward compatibility)
    claude_api_key: str = os.getenv("CLAUDE_API_KEY", "")
    claude_model: str = os.getenv("CLAUDE_MODEL", "claude-3-sonnet-20240229")

    # Database Settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql://localhost/course_companion")

    # Application Settings
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Feature Flags
    enable_premium_features: bool = os.getenv("ENABLE_PREMIUM_FEATURES", "true").lower() == "true"

    # Token Usage Limits
    token_usage_limit_per_user_per_day: int = int(os.getenv("TOKEN_USAGE_LIMIT_PER_USER_PER_DAY", "100000"))

    # Premium Pricing
    premium_tier_cost_per_thousand_tokens: float = float(os.getenv("PREMIUM_TIER_COST_PER_THOUSAND_TOKENS", "0.015"))

    # Cloud Storage
    cloudflare_account_id: str = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
    cloudflare_r2_access_key_id: str = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID", "")
    cloudflare_r2_secret_access_key: str = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY", "")
    cloudflare_r2_bucket_name: str = os.getenv("CLOUDFLARE_R2_BUCKET_NAME", "")

    class Config:
        env_file = ".env"

settings = Settings()