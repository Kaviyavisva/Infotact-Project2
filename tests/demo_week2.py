from src.recommendation_engine import RecommendationEngine
from src.report_generator import ReportGenerator

def run_week2_demo():
    print("--- Autonomous Disruption Monitoring Agent: Week 2 Demo ---\n")
    
    # 1. Initialize Engines
    print("[*] Initializing Recommendation Engine & Report Generator...")
    rec_engine = RecommendationEngine()
    report_gen = ReportGenerator()
    
    # 2. Simulated Input (This comes from the output of the Week 1 / Classifier module)
    simulated_disruption = {
        "disruption_type": "Strike",
        "impact_level": "Severe",
        "affected_supplier": "Oceanic Logistics Corp",
        "affected_location": "Port of Hamburg",
        "transportation_mode": "Ocean",
        "industry": "Retail"
    }
    
    print("\n[*] Received Disruption Context (From Classifier):")
    import json
    print(json.dumps(simulated_disruption, indent=2))
    
    # 3. Generate Recommendations
    print("\n[*] Generating Prioritized Recommendations...")
    try:
        recommendations = rec_engine.generate_recommendations(simulated_disruption)
        print(f"[+] Successfully generated {len(recommendations)} recommendations!")
        for rec in recommendations:
            print(f"    - [{rec.priority}] {rec.action} ({rec.estimated_time})")
            print(f"      Reason: {rec.reason}")
    except Exception as e:
        print(f"[-] Recommendation Generation Failed: {e}")
        return

    # 4. Generate Final Structured Report
    print("\n[*] Compiling Final Structured Mitigation Report...")
    try:
        report = report_gen.generate_report(
            # Using the validated context object created internally, but we can pass raw dict 
            # to be cleanly parsed if we adapt the signature.
            # But generate_report expects a DisruptionContext. Let's create it.
            context=rec_engine.generate_recommendations.__annotations__['return'], # Mocking type hint check
            recommendations=recommendations
        )
    except Exception as e:
        # We need to construct the context object first since `generate_report` takes the Pydantic object
        pass
    
    from src.recommendation_engine import DisruptionContext
    context_obj = DisruptionContext(**simulated_disruption)
    
    report = report_gen.generate_report(context_obj, recommendations)
    
    # 5. Export to JSON (Ready for LLM/LangGraph ingestion)
    final_json = report_gen.export_to_json(report, pretty=True)
    
    print("\n[*] Final Output JSON:\n")
    print(final_json)
    
if __name__ == "__main__":
    run_week2_demo()
