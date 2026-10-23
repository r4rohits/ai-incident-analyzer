
from fastapi import APIRouter, HTTPException

from app.models.incident import Incident
from app.services.incident_service import IncidentService
from app.services.exceptions import (
    AIConfigurationError,
    AIProviderError,
    AIResponseError,
)


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)

incidentservice = IncidentService()


@router.post(
    "/analyze",
    responses={
        502: {"description": "AI provider or response failure"},
        503: {"description": "AI analysis is not configured"},
    },
)
def analyze(incident: Incident):
    try:
        return incidentservice.analyze(incident)

    except AIConfigurationError as exc:
        raise HTTPException(
            status_code=503,
            detail="AI analysis is not configured.",
        ) from exc

    except (AIProviderError, AIResponseError) as exc:
        raise HTTPException(
            status_code=502,
            detail="AI analysis could not be completed.",
        ) from exc
