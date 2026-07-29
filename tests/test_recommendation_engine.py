import pytest
from src.recommendation_engine import RecommendationEngine, RecommendationError, DisruptionContext

@pytest.fixture
def engine():
    return RecommendationEngine()

def test_normal_disruption(engine):
    context = {
        "disruption_type": "Weather",
        "impact_level": "Medium",
        "affected_supplier": "GlobalTech Inc",
        "affected_location": "Shenzhen",
        "transportation_mode": "Ocean",
        "industry": "Electronics"
    }
    
    recs = engine.generate_recommendations(context)
    
    assert len(recs) > 0
    actions = [r.action for r in recs]
    assert "Safety stock increase" in actions
    
def test_severe_disruption_tie_breaker(engine):
    # This will trigger multiple criticals (Strike/Ocean -> Critical)
    # The tie-breaker should shift one to High
    context = {
        "disruption_type": "Strike",
        "impact_level": "Severe",
        "affected_supplier": "AutoParts Co",
        "affected_location": "Port of Los Angeles",
        "transportation_mode": "Ocean",
        "industry": "Automotive"
    }
    
    recs = engine.generate_recommendations(context)
    
    # Validation should pass
    val_sum = engine.validate_recommendations(recs)
    assert val_sum["is_valid"] is True
    assert val_sum["priorities_verified"] is True
    
    # Priority deduplication check
    priorities = [r.priority for r in recs]
    assert len(priorities) == len(set(priorities))  # No duplicates

def test_unknown_impact_level(engine):
    context = {
        "disruption_type": "Geopolitical",
        "impact_level": "Catastrophic", # Invalid
        "affected_supplier": "Supplier A",
        "affected_location": "Region B"
    }
    
    with pytest.raises(RecommendationError) as exc:
        engine.generate_recommendations(context)
    assert "Unknown impact level" in str(exc.value)

def test_missing_fields(engine):
    context = {
        "disruption_type": "Weather",
        "impact_level": "High"
    }
    with pytest.raises(RecommendationError):
        engine.generate_recommendations(context)

def test_validation_logic(engine):
    # Pass an empty list to validation
    val = engine.validate_recommendations([])
    assert val["is_valid"] is False
    assert "empty" in val["errors"][0]

def test_new_disruption_types(engine):
    types = ["Cyberattack", "Equipment failure", "Transportation delay", "Supplier shutdown", "Port congestion", "Inventory shortage"]
    for dtype in types:
        context = {
            "disruption_type": dtype,
            "impact_level": "Medium",
            "affected_supplier": "Test Co",
            "affected_location": "Test Loc"
        }
        recs = engine.generate_recommendations(context)
        assert len(recs) > 0
        
        val_sum = engine.validate_recommendations(recs)
        assert val_sum["is_valid"] is True
