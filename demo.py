from src.data_processor import DataProcessor
from src.output_formatter import OutputFormatter
import json

def run_demo():
    print("--- Autonomous Disruption Monitoring Agent: Week 1 Demo ---\n")
    
    # 1. Initialize Processor (this would typically sit between the news fetcher and classifier)
    print("[*] Initializing Data Processor...")
    processor = DataProcessor()
    
    # 2. Simulated input from News Fetcher
    raw_article_from_fetcher = {
        "title": "  Massive   Port Strike in   Los Angeles affecting retail  <br>",
        "content": "A massive strike at the Port of Los Angeles has caused severe delays. The retail industry is bracing for impact ahead of the holiday season.",
        "source": "Supply Chain Dive",
        "published_date": "October 26, 2023",
        "url": "https://example.com/logistics/la-port-strike-2023",
        "author": "Jane Smith",
        "country": "United States", # Might be provided, or might need extraction
    }
    
    print("\n[*] Raw Input from News Fetcher:")
    print(json.dumps(raw_article_from_fetcher, indent=2))
    
    # 3. Process the Data
    print("\n[*] Processing Data (Cleaning, Normalizing, Entity Extraction)...")
    try:
        processed_article = processor.process_article(raw_article_from_fetcher)
        print("[+] Processing Successful!")
    except Exception as e:
        print(f"[-] Processing Failed: {e}")
        return

    # 4. Format Output for next stage (Classifier / Week 2)
    print("\n[*] Formatting Output to Standardized JSON for LLM Classifier...")
    json_output = OutputFormatter.format_to_json(processed_article, pretty=True)
    
    print("\n[*] Final Output JSON:\n")
    print(json_output)
    
if __name__ == "__main__":
    run_demo()
