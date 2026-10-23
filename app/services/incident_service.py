from app.models.incident import Incident
from app.models.analysis_result import AnalysisResult
from app.services.parser import Parser
from app.services.prompt_builder import PromptBuilder
from app.services.llm_service import LLMService


class IncidentService:

    def __init__(self):
        self.parser = Parser()
        self.prompt_builder = PromptBuilder()

    def analyze(self, incident: Incident) -> AnalysisResult:
        parsed = self.parser.parse(incident)
        prompt = self.prompt_builder.build(parsed)

        llm_service = LLMService()
        result = llm_service.analyze(prompt)

        return result
