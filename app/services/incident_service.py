from app.models.incident import Incident
from app.models.analysis_result import AnalysisResult
from app.services.parser import Parser
from app.services.prompt_builder import PromptBuilder
from app.services.ai_provider_factory import AIProviderFactory


class IncidentService:

    def __init__(self):
        self.parser = Parser()
        self.prompt_builder = PromptBuilder()

    def analyze(self, incident: Incident) -> AnalysisResult:
        parsed = self.parser.parse(incident)
        prompt = self.prompt_builder.build(parsed)

        ai_provider = AIProviderFactory.create()
        result = ai_provider.analyze(prompt)

        return result
