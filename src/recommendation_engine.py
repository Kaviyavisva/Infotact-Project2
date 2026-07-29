import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError
from src.utils.logger import get_logger

logger = get_logger(__name__)

class RecommendationError(Exception):
    """Custom exception for recommendation engine errors and validation failures."""
    pass

class DisruptionContext(BaseModel):
    """
    Data model representing the context of a supply chain disruption.
    This acts as the input to the Recommendation Engine.
    """
    disruption_type: str = Field(..., description="Category of disruption (e.g., Strike, Weather, Geopolitical, Cyberattack)")
    impact_level: str = Field(..., description="Severity of impact: Low, Medium, High, Severe")
    affected_supplier: str = Field(..., description="Name of the affected supplier")
    affected_location: str = Field(..., description="Location (City/Port/Region) of the disruption")
    transportation_mode: Optional[str] = Field(None, description="Mode of transport affected (e.g., Ocean, Air, Rail, Road)")
    industry: Optional[str] = Field(None, description="Industry domain")

    @field_validator('impact_level')
    def validate_impact_level(cls, v):
        allowed = {"Low", "Medium", "High", "Severe"}
        # Normalize to title case just to be safe
        v = str(v).title()
        if v not in allowed:
            raise ValueError(f"Unknown impact level: {v}. Must be one of {allowed}")
        return v
        
    @field_validator('disruption_type', 'affected_supplier', 'affected_location')
    def check_not_empty(cls, v, info):
        if not v or not str(v).strip():
            raise ValueError(f"{info.field_name} cannot be empty or missing.")
        return v

class Recommendation(BaseModel):
    """
    Data model for a single mitigation recommendation.
    """
    action: str = Field(..., description="The recommended action")
    priority: str = Field(..., description="Priority: Critical, High, Medium, Low")
    estimated_time: str = Field(..., description="Estimated implementation time")
    expected_benefit: str = Field(..., description="The expected positive outcome of this action")
    reason: str = Field(..., description="Contextual reason why this recommendation was made")

class RecommendationEngine:
    """
    Analyzes supply chain disruptions and generates prioritized mitigation recommendations.
    Uses a configurable rule-based mapping system.
    """
    def __init__(self, custom_rules: Optional[List[Dict[str, Any]]] = None):
        """
        Initializes the engine. Loads default rules or overrides them with custom rules.
        """
        self.rules = custom_rules if custom_rules else self._load_default_rules()
        logger.info(f"RecommendationEngine initialized with {len(self.rules)} rules.")

    def _load_default_rules(self) -> List[Dict[str, Any]]:
        """
        Loads the default configurable recommendation rules.
        In a production environment, these could be loaded from a JSON/YAML file or a DB.
        """
        return [
            {
                "trigger": {"disruption_type": "Strike", "transportation_mode": "Ocean"},
                "action": "Port diversion",
                "estimated_time": "24-48 hours",
                "expected_benefit": "Avoids cargo stranding at striking port."
            },
            {
                "trigger": {"disruption_type": "Weather", "transportation_mode": "Air"},
                "action": "Airport diversion",
                "estimated_time": "12-24 hours",
                "expected_benefit": "Bypasses severe weather zones ensuring timely delivery."
            },
            {
                "trigger": {"disruption_type": "Cyberattack"},
                "action": "Manual system override",
                "estimated_time": "4-8 hours",
                "expected_benefit": "Restores basic operations while systems are secured."
            },
            {
                "trigger": {"disruption_type": "Equipment failure"},
                "action": "Dispatch maintenance crews",
                "estimated_time": "12-48 hours",
                "expected_benefit": "Minimizes downtime of critical machinery."
            },
            {
                "trigger": {"disruption_type": "Transportation delay"},
                "action": "Expedite priority shipments",
                "estimated_time": "24 hours",
                "expected_benefit": "Ensures critical components arrive despite delays."
            },
            {
                "trigger": {"disruption_type": "Supplier shutdown"},
                "action": "Activate secondary suppliers",
                "estimated_time": "48-72 hours",
                "expected_benefit": "Re-establishes supply line immediately."
            },
            {
                "trigger": {"disruption_type": "Port congestion"},
                "action": "Reroute to secondary ports",
                "estimated_time": "2-3 days",
                "expected_benefit": "Bypasses unloading bottlenecks."
            },
            {
                "trigger": {"disruption_type": "Inventory shortage"},
                "action": "Ration existing inventory",
                "estimated_time": "Immediate",
                "expected_benefit": "Prevents complete stockouts for high-margin products."
            },
            {
                "trigger": {"impact_level": ["High", "Severe"]},
                "action": "Alternative suppliers",
                "estimated_time": "1-2 weeks",
                "expected_benefit": "Diversifies supply chain risk and restores component flow."
            },
            {
                "trigger": {"impact_level": ["High", "Severe"], "industry": "Retail"},
                "action": "Warehouse redistribution",
                "estimated_time": "3-5 days",
                "expected_benefit": "Balances inventory across unaffected regions."
            },
            {
                "trigger": {"disruption_type": "Geopolitical"},
                "action": "Emergency procurement",
                "estimated_time": "1 week",
                "expected_benefit": "Secures critical materials before embargos or sanctions take effect."
            },
            {
                "trigger": {"impact_level": ["Medium", "High", "Severe"]},
                "action": "Safety stock increase",
                "estimated_time": "1-3 months",
                "expected_benefit": "Buffers against prolonged lead times."
            },
            {
                "trigger": {"impact_level": ["Low", "Medium"]},
                "action": "Shipment rescheduling",
                "estimated_time": "24 hours",
                "expected_benefit": "Avoids minor delays without incurring routing costs."
            },
            {
                "trigger": {"disruption_type": "Any"}, # Generic fallback
                "action": "Risk monitoring",
                "estimated_time": "Immediate",
                "expected_benefit": "Maintains situational awareness for further escalation."
            }
        ]

    def _determine_priority(self, impact_level: str, action: str) -> str:
        """
        Dynamically calculates priority based on impact level and the action type.
        """
        if impact_level == "Severe":
            return "Critical" if action in ["Alternative suppliers", "Port diversion", "Emergency procurement"] else "High"
        elif impact_level == "High":
            return "High" if action != "Risk monitoring" else "Medium"
        elif impact_level == "Medium":
            return "Medium"
        else:
            return "Low"

    def _format_reason(self, action: str, context: DisruptionContext) -> str:
        """
        Generates a contextual reason string for the recommendation based on the event details.
        """
        if action == "Alternative suppliers":
            return f"Due to the {context.impact_level.lower()} impact at {context.affected_supplier}, sourcing alternatives is critical."
        elif action in ["Port diversion", "Airport diversion", "Alternative transportation routes"]:
            mode = context.transportation_mode if context.transportation_mode else "transport"
            return f"{context.disruption_type} at {context.affected_location} has halted {mode.lower()} logistics."
        elif action == "Warehouse redistribution":
            return f"Impact at {context.affected_location} requires shifting inventory to unaffected regions."
        elif action == "Safety stock increase":
            return f"Ongoing {context.disruption_type} issues require higher baseline inventory for {context.affected_supplier} components."
        elif action == "Emergency procurement":
            return f"{context.impact_level} disruption at {context.affected_location} demands immediate spot-buying."
        else:
            return f"Standard mitigation protocol for a {context.impact_level.lower()} {context.disruption_type} event at {context.affected_location}."

    def validate_recommendations(self, recommendations: List[Recommendation]) -> Dict[str, Any]:
        """
        Validates the generated recommendations for correctness, completeness, 
        priority assignment, and ordering.
        Returns a validation summary dict.
        """
        summary = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "priorities_verified": False,
            "completeness_verified": False
        }
        
        if not recommendations:
            summary["is_valid"] = False
            summary["errors"].append("Recommendation list is empty.")
            return summary

        # Completeness Check
        for i, rec in enumerate(recommendations):
            if not all([rec.action, rec.priority, rec.estimated_time, rec.expected_benefit, rec.reason]):
                summary["is_valid"] = False
                summary["errors"].append(f"Recommendation {i+1} is missing fields.")
                
        summary["completeness_verified"] = len(summary["errors"]) == 0

        # Priority Verification (Ordering and Duplicates)
        priority_map = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        seen_priorities = set()
        prev_priority_val = -1
        
        for i, rec in enumerate(recommendations):
            p_val = priority_map.get(rec.priority, 4)
            
            # Check ordering
            if p_val < prev_priority_val:
                summary["is_valid"] = False
                summary["errors"].append(f"Ordering error: {rec.priority} appears after lower priority.")
            prev_priority_val = p_val
            
            # Check duplicates
            if p_val in seen_priorities:
                summary["is_valid"] = False
                summary["errors"].append(f"Duplicate priority detected: {rec.priority}.")
            seen_priorities.add(p_val)
            
        summary["priorities_verified"] = len(summary["errors"]) == 0

        if summary["is_valid"]:
            logger.info("Validation completed successfully: Recommendations are complete and correctly ordered.")
        else:
            logger.warning(f"Validation failed with errors: {summary['errors']}")
            
        return summary

    def generate_recommendations(self, raw_context: Dict[str, Any]) -> List[Recommendation]:
        """
        Validates input and generates a list of prioritized recommendations.
        """
        import time
        start_time = time.time()
        logger.debug(f"Received input for recommendations: {raw_context}")
        
        # 1. Validation
        try:
            context = DisruptionContext(**raw_context)
        except ValidationError as e:
            logger.error(f"Input validation failed: {e.errors()}")
            raise RecommendationError(f"Malformed input data: {e.errors()}")
        
        logger.info(f"Generating recommendations for {context.impact_level} {context.disruption_type} at {context.affected_location}.")
        
        generated_recs = []
        seen_actions = set()

        # 2. Rule Evaluation
        for rule in self.rules:
            trigger = rule.get("trigger", {})
            action = rule.get("action")
            
            # Avoid duplicate recommendations
            if action in seen_actions:
                continue

            match = True
            
            # Check all conditions in the trigger
            for key, condition_val in trigger.items():
                if key == "disruption_type" and condition_val == "Any":
                    continue # Always matches
                
                context_val = getattr(context, key, None)
                
                if isinstance(condition_val, list):
                    if context_val not in condition_val:
                        match = False
                        break
                elif context_val != condition_val:
                    match = False
                    break
                    
            if match:
                priority = self._determine_priority(context.impact_level, action)
                reason = self._format_reason(action, context)
                
                rec = Recommendation(
                    action=action,
                    priority=priority,
                    estimated_time=rule.get("estimated_time", "Unknown"),
                    expected_benefit=rule.get("expected_benefit", "General risk mitigation."),
                    reason=reason
                )
                generated_recs.append(rec)
                seen_actions.add(action)
                logger.debug(f"Rule triggered: {action}")

        # 3. Final validation on output
        if not generated_recs:
            logger.warning("No recommendations generated. Applying generic fallback.")
            # Fallback in case rules completely misfire (though "Any" rule prevents this usually)
            fallback = Recommendation(
                action="Risk monitoring",
                priority=self._determine_priority(context.impact_level, "Risk monitoring"),
                estimated_time="Immediate",
                expected_benefit="Maintains situational awareness.",
                reason=self._format_reason("Risk monitoring", context)
            )
            generated_recs.append(fallback)

        # Sort by priority (Critical > High > Medium > Low)
        priority_map = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        generated_recs.sort(key=lambda x: priority_map.get(x.priority, 4))
        
        # Priority Deduplication Algorithm (Tie-breaker)
        # Ensure no two recommendations share the exact same priority by shifting duplicates down.
        # This guarantees strict uniqueness in priority levels as per requirements.
        used_priorities = set()
        deduped_recs = []
        for rec in generated_recs:
            original_priority = rec.priority
            current_p_val = priority_map.get(original_priority, 4)
            
            # If the priority is already used, find the next available lower priority
            while current_p_val in used_priorities and current_p_val <= 3:
                current_p_val += 1
                
            # If current_p_val > 3, we have run out of distinct priority levels (only 4 exist).
            # To strictly satisfy the "No duplicate priorities" requirement, we must discard it.
            if current_p_val > 3:
                logger.debug(f"Discarded recommendation '{rec.action}' due to priority saturation.")
                continue
                
            # Map back to string
            new_priority = {0: "Critical", 1: "High", 2: "Medium", 3: "Low"}.get(current_p_val)
            
            if new_priority != original_priority:
                rec.priority = new_priority
                logger.debug(f"Priority tie-breaker applied: shifted {rec.action} to {new_priority}")
                
            used_priorities.add(current_p_val)
            deduped_recs.append(rec)

        # Final sort to ensure they are strictly ordered after deduplication
        deduped_recs.sort(key=lambda x: priority_map.get(x.priority, 4))

        exec_time = (time.time() - start_time) * 1000
        logger.info(f"Successfully generated {len(deduped_recs)} prioritized recommendations in {exec_time:.2f}ms.")
        return deduped_recs
