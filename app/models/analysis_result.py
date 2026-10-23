from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    likely_issue: str
    possible_impact: str
    recommended_action: str
    confidence: float = Field(ge=0, le=1)
    missing_information: list[str]
