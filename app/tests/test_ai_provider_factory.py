
import pytest

from app.services.ai_provider_factory import AIProviderFactory
from app.services.llm_service import LLMService
from app.services.exceptions import AIConfigurationError


def test_factory_returns_openai_service_by_default(monkeypatch):
    monkeypatch.delenv("AI_PROVIDER", raising=False)

    provider = AIProviderFactory.create()

    assert isinstance(provider, LLMService)


def test_factory_rejects_unsupported_provider(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "unsupported")

    with pytest.raises(AIConfigurationError):
        AIProviderFactory.create()

def test_factory_returns_gemini_service(monkeypatch):
    from app.services.gemini_service import GeminiService

    monkeypatch.setenv("AI_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-flash")

    provider = AIProviderFactory.create()

    assert isinstance(provider, GeminiService)