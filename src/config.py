from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_FILE = BASE_DIR / "output" / "news.json"
LOG_FILE = BASE_DIR / "logs" / "news_fetcher.log"

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MAX_RESULTS = 10

SEARCH_QUERY = (
    "latest logistics OR supply chain disruption "
    "shipping delay port congestion freight disruption"
)