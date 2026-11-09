
import os
import logging

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.models.analysis_result import AnalysisResult
from app.services.exceptions import (
    AIConfigurationError,
    AIProviderError,
    AIResponseError,
)

logger = logging.getLogger(__name__)
load_dotenv()


class GeminiService:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        model = os.getenv("GEMINI_MODEL")

        if not api_key or api_key == "your_gemini_key_here":
            raise AIConfigurationError(
                "Gemini API key is not configured."
            )

        if not model:
            raise AIConfigurationError(
                "GEMINI_MODEL is not configured."
            )

        self.model = model
        self.client = genai.Client(api_key=api_key)

    def analyze(self, prompt: str) -> AnalysisResult:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=AnalysisResult,
                ),
            )

        except Exception as exc:
            logger.exception("Gemini API request failed")
            raise AIProviderError(
                "The Gemini provider could not complete the request."
            ) from exc

        if response.parsed is None:
            logger.error("Gemini response did not contain parsed output")
            raise AIResponseError(
                "The model did not return a parsed analysis."
            )

        try:
            return AnalysisResult.model_validate(response.parsed)
        except Exception as exc:
            logger.exception("Gemini returned an invalid analysis")
            raise AIResponseError(
                "The Gemini response did not match the expected structure."
            ) from exc
