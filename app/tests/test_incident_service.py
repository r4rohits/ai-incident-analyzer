from unittest.mock import Mock

from app.models.incident import Incident, Severity
from app.models.analysis_result import AnalysisResult
from app.services.incident_service import IncidentService


def test_analyze_returns_llm_result(monkeypatch):
    expected_result = AnalysisResult(
        likely_issue="Database connection interruption",
        possible_impact="Payment requests may fail",
        recommended_action="Check database connectivity",
        confidence=0.85,
        missing_information=[],
    )

    mock_provider = Mock()
    mock_provider.analyze.return_value = expected_result

    monkeypatch.setattr(
        "app.services.incident_service.AIProviderFactory.create",
        lambda: mock_provider,
    )

    service = IncidentService()

    incident = Incident(
        service="payment-service",
        severity=Severity.ERROR,
        message="Database connection was lost",
        count=5,
    )

    result = service.analyze(incident)

    assert result == expected_result
    mock_provider.analyze.assert_called_once()
