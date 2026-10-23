
import os

from dotenv import load_dotenv
from openai import (
    OpenAI,
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    OpenAIError,
)

from app.models.analysis_result import AnalysisResult
from app.services.exceptions import (
    AIConfigurationError,
    AIProviderError,
    AIResponseError,
)


load_dotenv()


class LLMService:

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL")

        if not api_key or api_key == "your_api_key_goes_here":
            raise AIConfigurationError(
                "OpenAI API key is not configured."
            )

        if not model:
            raise AIConfigurationError(
                "OPENAI_MODEL is not configured."
            )

        self.model = model
        self.client = OpenAI(
            api_key=api_key,
            timeout=20.0,
            max_retries=1,
        )

    def analyze(self, prompt: str) -> AnalysisResult:
        try:
            response = self.client.responses.parse(
                model=self.model,
                input=prompt,
                text_format=AnalysisResult,
            )

        except APITimeoutError as exc:
            raise AIProviderError(
                "The AI analysis request timed out."
            ) from exc

        except APIConnectionError as exc:
            raise AIProviderError(
                "Unable to connect to the AI provider."
            ) from exc

        except APIStatusError as exc:
            raise AIProviderError(
                f"The AI provider returned HTTP {exc.status_code}."
            ) from exc

        except OpenAIError as exc:
            raise AIProviderError(
                "The AI provider could not complete the request."
            ) from exc

        if response.output_parsed is None:
            raise AIResponseError(
                "The model did not return a parsed analysis."
            )

        return response.output_parsed
