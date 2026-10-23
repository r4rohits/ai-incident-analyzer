from enum import Enum
from pydantic import BaseModel, Field


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Incident(BaseModel):
    service: str = Field(..., min_length=1)
    severity: Severity
    message: str = Field(..., min_length=1)
    count: int = Field(default=1, ge=1)