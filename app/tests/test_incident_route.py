
from fastapi.testclient import TestClient

from app.main import app
from app.routes.incidents import incidentservice
from app.services.exceptions import (
    AIConfigurationError,
    AIProviderError,
    AIResponseError,
)

client = TestClient(app)

INCIDENT_PAYLOAD = {
    "service": "payment-service",
    "severity": "ERROR",
    "message": "Database connection was lost",
    "count": 5,
}


def test_configuration_error_returns_503(monkeypatch):
    def raise_configuration_error(incident):
        raise AIConfigurationError("Missing API key")

    monkeypatch.setattr(
        incidentservice,
        "analyze",
        raise_configuration_error,
    )

    response = client.post(
        "/incidents/analyze",
        json=INCIDENT_PAYLOAD,
    )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "AI analysis is not configured."
    )


def test_provider_error_returns_502(monkeypatch):
    def raise_provider_error(incident):
        raise AIProviderError("Provider unavailable")

    monkeypatch.setattr(
        incidentservice,
        "analyze",
        raise_provider_error,
    )

    response = client.post(
        "/incidents/analyze",
        json=INCIDENT_PAYLOAD,
    )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "AI analysis could not be completed."
    )


def test_unusable_response_returns_502(monkeypatch):
    def raise_response_error(incident):
        raise AIResponseError("No parsed response")

    monkeypatch.setattr(
        incidentservice,
        "analyze",
        raise_response_error,
    )

    response = client.post(
        "/incidents/analyze",
        json=INCIDENT_PAYLOAD,
    )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "AI analysis could not be completed."
    )
