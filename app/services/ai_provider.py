
from typing import Protocol

from app.models.analysis_result import AnalysisResult


class AIProvider(Protocol):

    def analyze(self, prompt: str) -> AnalysisResult:
        ...
