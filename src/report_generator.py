import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

from src.utils.logger import get_logger
from src.recommendation_engine import Recommendation, DisruptionContext

logger = get_logger(__name__)

class ReportError(Exception):
    """Custom exception for report generation errors."""
    pass

class StructuredReport(BaseModel):
    """
    Data model for the final structured mitigation report.
    This schema is designed to be easily consumed by dashboards, REST APIs, or LLM agents.
    """
    incident_summary: str = Field(..., description="High-level summary of the incident")
    affected_region: str = Field(..., description="The region or specific location affected")
    affected_supplier: str = Field(..., description="The supplier facing the disruption")
    disruption_type: str = Field(..., description="Category of disruption")
    impact_level: str = Field(..., description="Severity of impact")
    risk_score: float = Field(..., description="Calculated risk score (0.0 to 10.0)")
    mitigation_recommendations: List[Recommendation] = Field(..., description="Prioritized recommendations")
    timestamp: str = Field(..., description="ISO 8601 timestamp of report generation")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context or system metadata")

class ReportGenerator:
    """
    Generates structured mitigation reports from disruption contexts and recommendations.
    Provides JSON export capabilities.
    """
    
    def __init__(self):
        logger.debug("ReportGenerator initialized.")

    def _calculate_risk_score(self, impact_level: str, num_recommendations: int) -> float:
        """
        Calculates a baseline risk score based on severity and the number of mitigations required.
        """
        base_scores = {
            "Low": 2.0,
            "Medium": 5.0,
            "High": 8.0,
            "Severe": 9.5
        }
        score = base_scores.get(impact_level.title(), 5.0)
        
        # Slightly inflate score if multiple mitigations are needed, cap at 10.0
        score += min((num_recommendations * 0.1), 0.5)
        return round(min(score, 10.0), 1)

    def generate_report(self, context: DisruptionContext, recommendations: List[Recommendation]) -> StructuredReport:
        """
        Compiles the context and recommendations into a StructuredReport.
        """
        if not recommendations:
            logger.error("Cannot generate report: recommendations list is empty.")
            raise ReportError("Recommendations cannot be empty when generating a report.")

        logger.info(f"Generating report for {context.affected_supplier} at {context.affected_location}.")
        
        # Auto-generate an incident summary
        mode_text = f" affecting {context.transportation_mode.lower()} transport" if context.transportation_mode else ""
        summary = f"A {context.impact_level.lower()} impact {context.disruption_type} disruption has been detected at {context.affected_location}, impacting operations for {context.affected_supplier}{mode_text}."

        risk_score = self._calculate_risk_score(context.impact_level, len(recommendations))
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        try:
            report = StructuredReport(
                incident_summary=summary,
                affected_region=context.affected_location,
                affected_supplier=context.affected_supplier,
                disruption_type=context.disruption_type,
                impact_level=context.impact_level,
                risk_score=risk_score,
                mitigation_recommendations=recommendations,
                timestamp=timestamp,
                metadata={"version": "1.0.0", "generator": "ReportGeneratorModule"}
            )
            logger.info("Successfully generated structured report object.")
            return report
            
        except ValidationError as e:
            logger.error(f"Report validation failed: {e.errors()}")
            raise ReportError(f"Failed to build valid report: {e.errors()}")

    def export_to_dict(self, report: StructuredReport) -> Dict[str, Any]:
        """
        Exports the StructuredReport to a Python dictionary format.
        Useful for passing directly to LangGraph agents or other Python services.
        """
        logger.debug("Exporting report to dictionary format.")
        # Uses Pydantic's model_dump to serialize nested objects correctly
        return report.model_dump()

    def export_to_json(self, report: StructuredReport, pretty: bool = True) -> str:
        """
        Exports the StructuredReport to a JSON string.
        
        Args:
            report: The StructuredReport object.
            pretty: If True, formats the JSON with indentation for readability.
        """
        import time
        start_time = time.time()
        logger.info(f"Exporting report to JSON. (Pretty: {pretty})")
        
        try:
            dict_data = self.export_to_dict(report)
            if pretty:
                json_str = json.dumps(dict_data, indent=4, ensure_ascii=False)
            else:
                json_str = json.dumps(dict_data, separators=(',', ':'), ensure_ascii=False)
                
            exec_time = (time.time() - start_time) * 1000
            logger.info(f"Report exported to JSON successfully in {exec_time:.2f}ms.")
            return json_str
        except TypeError as e:
            logger.error(f"JSON serialization failed: {e}")
            raise ReportError(f"Failed to serialize report to JSON: {e}")

    def validate_report(self, json_str: str) -> Dict[str, Any]:
        """
        Validates an exported JSON report.
        Checks for parseability, schema consistency, and completeness.
        Returns a validation summary dict.
        """
        summary = {
            "is_valid": True,
            "errors": [],
            "json_parsed": False,
            "schema_verified": False
        }
        
        # 1. JSON Parseability
        try:
            parsed_data = json.loads(json_str)
            summary["json_parsed"] = True
        except json.JSONDecodeError as e:
            summary["is_valid"] = False
            summary["errors"].append(f"Malformed JSON: {e}")
            return summary
            
        # 2. Schema and Completeness Verification
        required_fields = [
            "incident_summary", "affected_supplier", "affected_region", 
            "disruption_type", "impact_level", "risk_score", 
            "mitigation_recommendations", "timestamp", "metadata"
        ]
        
        for field in required_fields:
            if field not in parsed_data:
                summary["is_valid"] = False
                summary["errors"].append(f"Missing required field in report: {field}")
            elif parsed_data[field] is None:
                summary["is_valid"] = False
                summary["errors"].append(f"Null value for required field: {field}")
                
        if parsed_data.get("mitigation_recommendations"):
            rec_fields = ["action", "priority", "estimated_time", "expected_benefit", "reason"]
            for i, rec in enumerate(parsed_data["mitigation_recommendations"]):
                for rf in rec_fields:
                    if rf not in rec:
                        summary["is_valid"] = False
                        summary["errors"].append(f"Recommendation {i+1} missing field: {rf}")
        else:
            summary["is_valid"] = False
            summary["errors"].append("Missing recommendations in report.")

        summary["schema_verified"] = len(summary["errors"]) == 0
        
        if summary["is_valid"]:
            logger.info("JSON Report validation completed successfully.")
        else:
            logger.warning(f"JSON Report validation failed: {summary['errors']}")
            
        return summary
