# Autonomous Disruption Monitoring Agent - Week 1

This repository contains the `data_processor` and `output_formatter` modules for Project 3 (Autonomous Disruption Monitoring Agent), developed during the Infotact Generative AI Internship.

## Architecture & Integration

These modules sit centrally in the pipeline:
`Web Search API -> News Fetcher -> [Data Processor] -> [Output Formatter] -> LLM Risk Classification -> Output`

1. **`news_fetcher.py` (Teammate's Module)** provides a raw dictionary of scraped news to our module.
2. **`data_processor.py`** takes this raw dictionary and applies:
   - Data validation (using Pydantic models).
   - Text cleaning (HTML stripping, whitespace normalization, unicode fixing).
   - Date normalization (ISO 8601).
   - Entity Extraction (Country, City, Port, Supplier Location, Industry) via spaCy and targeted fallbacks.
   - Duplicate Detection (hashing, similarity scoring).
3. **`output_formatter.py`** converts the cleaned and validated `ProcessedArticle` object into a standardized, production-ready JSON structure.
4. **`classifier.py` (Teammate's Module)** receives this JSON structure for LLM classification in Week 2.

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Download the required spaCy English model:
   ```bash
   python -m spacy download en_core_web_sm
   ```
3. (Optional) Copy `.env.example` to `.env` to override default configurations like Log Level and Similarity Threshold.

## Usage Example

Run the included `demo.py` to see the modules in action, simulating the hand-off from the News Fetcher.

```bash
python demo.py
```

### Example Input (from News Fetcher)
```json
{
  "title": "  Massive   Port Strike in   Los Angeles affecting retail  <br>",
  "content": "A massive strike at the Port of Los Angeles has caused severe delays. The retail industry is bracing for impact ahead of the holiday season.",
  "source": "Supply Chain Dive",
  "published_date": "October 26, 2023",
  "url": "https://example.com/logistics/la-port-strike-2023",
  "author": "Jane Smith",
  "country": "United States"
}
```

### Example Processed Output (JSON from Output Formatter)
```json
{
  "article_id": "c1f7b8a...",
  "title": "Massive Port Strike in Los Angeles affecting retail",
  "source": "Supply Chain Dive",
  "published_date": "2023-10-26T00:00:00",
  "entities": {
      "country": "United States",
      "city": null,
      "port": "Los Angeles",
      "supplier_location": null,
      "industry": "Retail"
  },
  "content": "A massive strike at the Port of Los Angeles has caused severe delays. The retail industry is bracing for impact ahead of the holiday season.",
  "metadata": {
      "language": "en",
      "processed_timestamp": "2023-10-26T15:30:00.000000Z",
      "version": "1.0.0"
  }
}
```

## Running Tests

Comprehensive unit tests are provided using `pytest` to ensure production readiness, checking happy paths, validation failures, and duplicate detection.

```bash
pytest tests/
```
