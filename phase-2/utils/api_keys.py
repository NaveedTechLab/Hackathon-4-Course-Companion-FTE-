import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class APIKeyManager:
    """
    Secure API key management for Claude integration
    """

    def __init__(self):
        self.claude_api_key = os.getenv("CLAUDE_API_KEY")
        if not self.claude_api_key:
            logger.warning("CLAUDE_API_KEY environment variable not set")

    def get_claude_api_key(self) -> Optional[str]:
        """
        Retrieve Claude API key from environment variables
        """
        return self.claude_api_key

    def validate_api_key(self, api_key: str) -> bool:
        """
        Validate API key format (basic validation)
        Claude API keys typically start with 'sk-'
        """
        if not api_key or not isinstance(api_key, str):
            return False

        # Basic format validation for Claude API keys
        if not api_key.startswith("sk-"):
            logger.warning(f"Invalid Claude API key format: {api_key[:10]}...")
            return False

        # Check for minimum length (Claude keys are typically longer)
        if len(api_key) < 20:
            logger.warning(f"API key appears to be too short: {api_key[:10]}...")
            return False

        return True

    def get_api_key_for_request(self) -> Optional[str]:
        """
        Get API key for making requests (with validation)
        """
        key = self.get_claude_api_key()
        if key and self.validate_api_key(key):
            return key
        return None


# Global instance
api_key_manager = APIKeyManager()


def get_claude_client_config():
    """
    Get configuration for Claude client initialization
    """
    api_key = api_key_manager.get_api_key_for_request()
    if not api_key:
        raise ValueError("Claude API key not available or invalid")

    # Get model from environment or use default
    model = os.getenv("CLAUDE_MODEL", "claude-3-sonnet-20240229")

    return {
        "api_key": api_key,
        "model": model,
        "max_tokens": 1000,
        "temperature": 0.7
    }