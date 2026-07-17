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
    
    assert isinstance(report, StructuredReport)
    assert report.affected_region == "Miami Port"
    assert report.affected_supplier == "Supplier X"
    assert report.risk_score > 0
    assert len(report.mitigation_recommendations) == 1
    assert "Weather" in report.incident_summary

def test_generate_report_empty_recommendations(report_generator, mock_context):
    with pytest.raises(ReportError) as exc:
        report_generator.generate_report(mock_context, [])
    assert "Recommendations cannot be empty" in str(exc.value)

def test_export_to_dict(report_generator, mock_context, mock_recommendations):
    report = report_generator.generate_report(mock_context, mock_recommendations)
    dict_report = report_generator.export_to_dict(report)
    
    assert isinstance(dict_report, dict)
    assert dict_report["affected_supplier"] == "Supplier X"
    assert isinstance(dict_report["mitigation_recommendations"], list)
    assert dict_report["mitigation_recommendations"][0]["action"] == "Port diversion"

def test_export_to_json_pretty(report_generator, mock_context, mock_recommendations):
    report = report_generator.generate_report(mock_context, mock_recommendations)
    json_str = report_generator.export_to_json(report, pretty=True)
    
    assert isinstance(json_str, str)
    assert "\n" in json_str
    assert "    " in json_str # check for indentation
    
    parsed = json.loads(json_str)
    assert parsed["risk_score"] > 0

def test_export_to_json_compact(report_generator, mock_context, mock_recommendations):
    report = report_generator.generate_report(mock_context, mock_recommendations)
    json_str = report_generator.export_to_json(report, pretty=False)
    
    assert isinstance(json_str, str)
    assert "\n" not in json_str
    assert '": ' not in json_str # check for compact separators
    assert '", "' not in json_str
    
    parsed = json.loads(json_str)
    assert parsed["incident_summary"] != ""
