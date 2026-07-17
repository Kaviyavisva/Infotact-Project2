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
    # Should trigger Safety stock increase and generic fallback (Risk monitoring)
    actions = [r.action for r in recs]
    assert "Safety stock increase" in actions
    assert "Risk monitoring" in actions
    
    # Check priorities are correctly sorted
    assert recs[0].priority in ["Medium", "High", "Critical"]

def test_severe_disruption(engine):
    context = {
        "disruption_type": "Strike",
        "impact_level": "Severe",
        "affected_supplier": "AutoParts Co",
        "affected_location": "Port of Los Angeles",
        "transportation_mode": "Ocean",
        "industry": "Automotive"
    }
    
    recs = engine.generate_recommendations(context)
    
    actions = [r.action for r in recs]
    assert "Port diversion" in actions
    assert "Alternative suppliers" in actions
    
    # Alternative suppliers should be Critical for Severe impact
    alt_supplier_rec = next(r for r in recs if r.action == "Alternative suppliers")
    assert alt_supplier_rec.priority == "Critical"
    assert "Critical" == recs[0].priority # Highest priority should be first

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
        # Missing supplier and location
    }
    
    with pytest.raises(RecommendationError) as exc:
        engine.generate_recommendations(context)
    assert "affected_supplier" in str(exc.value)

def test_unrecognized_disruption_triggers_fallback(engine):
    context = {
        "disruption_type": "Alien Invasion",
        "impact_level": "Low",
        "affected_supplier": "Earth Corp",
        "affected_location": "Global"
    }
    
    recs = engine.generate_recommendations(context)
    assert len(recs) > 0
    
    actions = [r.action for r in recs]
    assert "Risk monitoring" in actions # Fallback 'Any' rule
    assert "Shipment rescheduling" in actions # Low impact triggers this

def test_empty_string_validation(engine):
    context = {
        "disruption_type": " ",
        "impact_level": "High",
        "affected_supplier": "Supplier",
        "affected_location": "Location"
    }
    with pytest.raises(RecommendationError) as exc:
        engine.generate_recommendations(context)
    assert "cannot be empty" in str(exc.value)
