
from app.models.incident import Incident, Severity
from app.models.parsed_incident import ParsedIncident
from app.services.parser import Parser


def test_normalize_lowercases_and_removes_punctuation():
    parser = Parser()

    result = parser.normalize(
        "The DATABASE connection was lost after 15 seconds!!!"
    )

    assert result == (
        "the database connection was lost after 15 seconds"
    )


def test_extract_keywords_removes_stop_words():
    parser = Parser()

    result = parser.extract_keywords(
        "the database connection was lost after 15 seconds"
    )

    assert result == [
        "database",
        "connection",
        "lost",
        "15",
        "seconds",
    ]


def test_parse_preserves_incident_fields():
    parser = Parser()

    incident = Incident(
        service="payment-service",
        severity=Severity.ERROR,
        message="The DATABASE connection was lost after 15 seconds!!!",
        count=5,
    )

    result = parser.parse(incident)

    assert isinstance(result, ParsedIncident)
    assert result.service == "payment-service"
    assert result.severity == Severity.ERROR
    assert result.count == 5
    assert result.normalized_message == (
        "the database connection was lost after 15 seconds"
    )
    assert result.keywords == [
        "database",
        "connection",
        "lost",
        "15",
        "seconds",
    ]


def test_normalize_collapses_repeated_whitespace():
    parser = Parser()

    result = parser.normalize(
        "  Database   connection\nwas\tlost  "
    )

    assert result == "database connection was lost"


def test_normalize_handles_punctuation_only():
    parser = Parser()

    result = parser.normalize("!!!...???")

    assert result == ""


def test_extract_keywords_returns_empty_list_for_empty_input():
    parser = Parser()

    result = parser.extract_keywords("")

    assert result == []
