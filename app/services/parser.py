import string

from app.models.incident import Incident
from app.models.parsed_incident import ParsedIncident


STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were",
    "after", "before", "and", "or", "to", "of", "in",
}


class Parser:

    def normalize(self, message: str) -> str:
        message = message.lower()

        message = message.translate(
            str.maketrans("", "", string.punctuation)
        )

        return " ".join(message.split())

    def extract_keywords(self, normalized_message: str) -> list[str]:
        words = normalized_message.split()

        return [
            word
            for word in words
            if word not in STOP_WORDS
        ]

    def parse(self, incident: Incident) -> ParsedIncident:
        normalized = self.normalize(incident.message)
        keywords = self.extract_keywords(normalized)

        return ParsedIncident(
            service=incident.service,
            severity=incident.severity,
            normalized_message=normalized,
            keywords=keywords,
            count=incident.count,
        )
