
import pytest

from app.services.gemini_service import GeminiService
from app.services.exceptions import AIConfigurationError
from unittest.mock import Mock

from app.models.analysis_result import AnalysisResult
from app.services.exceptions import AIProviderError, AIResponseError


def test_missing_gemini_api_key_raises_configuration_error(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-flash")

    with pytest.raises(AIConfigurationError):
        GeminiService()


def test_missing_gemini_model_raises_configuration_error(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")
    monkeypatch.delenv("GEMINI_MODEL", raising=False)

    with pytest.raises(AIConfigurationError):
        GeminiService()


def test_analyze_returns_valid_analysis_result(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-flash")

    expected_result = AnalysisResult(
        likely_issue="Database connection failure",
        possible_impact="Payment requests may fail",
        recommended_action="Check database connectivity",
        confidence=0.90,
        missing_information=[],
    )

    mock_response = Mock()
    mock_response.parsed = expected_result

    mock_client = Mock()
    mock_client.models.generate_content.return_value = mock_response

    monkeypatch.setattr(
        "app.services.gemini_service.genai.Client",
        lambda api_key: mock_client,
    )

    service = GeminiService()
    result = service.analyze("Analyze this incident")

    assert result == expected_result
    mock_client.models.generate_content.assert_called_once()


def test_analyze_raises_error_for_empty_response(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-flash")

    mock_response = Mock()
    mock_response.parsed = None

    mock_client = Mock()
    mock_client.models.generate_content.return_value = mock_response

    monkeypatch.setattr(
        "app.services.gemini_service.genai.Client",
        lambda api_key: mock_client,
    )

    service = GeminiService()

    with pytest.raises(AIResponseError):
        service.analyze("Analyze this incident")


def test_analyze_raises_provider_error_on_api_failure(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-flash")

    mock_client = Mock()
    mock_client.models.generate_content.side_effect = Exception(
        "Simulated Gemini API failure"
    )

    monkeypatch.setattr(
        "app.services.gemini_service.genai.Client",
        lambda api_key: mock_client,
    )

    service = GeminiService()

    with pytest.raises(AIProviderError):
        service.analyze("Analyze this incident")
