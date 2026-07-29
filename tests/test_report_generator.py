import pytest
import json
from src.recommendation_engine import DisruptionContext, Recommendation
from src.report_generator import ReportGenerator, ReportError, StructuredReport

@pytest.fixture
def report_generator():
    return ReportGenerator()

@pytest.fixture
def mock_context():
    return DisruptionContext(
        disruption_type="Weather",
        impact_level="High",
        affected_supplier="Supplier X",
        affected_location="Miami Port",
        transportation_mode="Ocean",
        industry="Retail"
    )

@pytest.fixture
def mock_recommendations():
    return [
        Recommendation(
            action="Port diversion",
            priority="High",
            estimated_time="24 hours",
            expected_benefit="Avoid hurricane path.",
            reason="Weather at Miami Port requires diversion."
        )
    ]

def test_generate_report_success(report_generator, mock_context, mock_recommendations):
    report = report_generator.generate_report(mock_context, mock_recommendations)
    assert report.affected_region == "Miami Port"
    assert len(report.mitigation_recommendations) == 1

def test_generate_report_empty_recommendations(report_generator, mock_context):
    with pytest.raises(ReportError):
        report_generator.generate_report(mock_context, [])

def test_validate_report_valid_json(report_generator, mock_context, mock_recommendations):
    report = report_generator.generate_report(mock_context, mock_recommendations)
    json_str = report_generator.export_to_json(report, pretty=True)
    
    val_sum = report_generator.validate_report(json_str)
    assert val_sum["is_valid"] is True
    assert val_sum["json_parsed"] is True
    assert val_sum["schema_verified"] is True

def test_validate_report_malformed_json(report_generator):
    bad_json = '{"incident_summary": "Incomplete json'
    val_sum = report_generator.validate_report(bad_json)
    assert val_sum["is_valid"] is False
    assert val_sum["json_parsed"] is False

def test_validate_report_missing_fields(report_generator):
    incomplete_json = json.dumps({
        "incident_summary": "Missing other fields"
    })
    val_sum = report_generator.validate_report(incomplete_json)
    assert val_sum["is_valid"] is False
    assert val_sum["json_parsed"] is True
    assert val_sum["schema_verified"] is False
    assert any("affected_supplier" in err for err in val_sum["errors"])
