
import pytest
from pydantic import ValidationError

from app.models.analysis_result import AnalysisResult


def test_valid_analysis_result_is_accepted():
    result = AnalysisResult(
        likely_issue="Database connection interruption",
        possible_impact="Payment requests may fail",
        recommended_action="Check database connectivity",
        confidence=0.85,
        missing_information=["Database error logs"],
    )

    assert result.confidence == 0.85
    assert result.missing_information == ["Database error logs"]


@pytest.mark.parametrize(
    "confidence",
    [-0.1, 1.1],
)
def test_confidence_outside_range_is_rejected(confidence):
    with pytest.raises(ValidationError):
        AnalysisResult(
            likely_issue="Unknown",
            possible_impact="Unknown",
            recommended_action="Investigate",
            confidence=confidence,
            missing_information=[],
        )


def test_missing_required_field_is_rejected():
    with pytest.raises(ValidationError):
        AnalysisResult(
            likely_issue="Database connection interruption",
            possible_impact="Payment requests may fail",
            recommended_action="Check database connectivity",
            confidence=0.85,
        )
