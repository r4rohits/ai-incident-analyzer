from pydantic import BaseModel

from app.models.incident import Severity


class ParsedIncident(BaseModel):
    service: str
    severity: Severity
    normalized_message: str
    keywords: list[str]
    count: int