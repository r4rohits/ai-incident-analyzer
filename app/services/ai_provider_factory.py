
import os

from app.services.llm_service import LLMService
from app.services.exceptions import AIConfigurationError
from app.services.gemini_service import GeminiService
from app.services.ai_provider import AIProvider


class AIProviderFactory:

    @staticmethod
    def create() -> AIProvider:
        provider = os.getenv("AI_PROVIDER", "openai").strip().lower()

        if provider == "openai":
            return LLMService()

        if provider == "gemini":
            return GeminiService()

        raise AIConfigurationError(
            f"Unsupported AI provider: {provider}"
        )
