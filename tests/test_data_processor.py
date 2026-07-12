import pytest
from src.data_processor import DataProcessor, ProcessedArticle, DataValidationError

@pytest.fixture
def processor():
    return DataProcessor()

@pytest.fixture
def valid_raw_article():
    return {
        "title": "  Major Delay at   Port of Shanghai <br> ",
        "content": "The <b>Port of Shanghai</b> is facing delays due to weather. Supply chains in the automotive industry are affected.",
        "source": "Logistics News",
        "published_date": "2023-10-25 14:30:00",
        "url": "https://example.com/news/123",
        "author": "John Doe",
        "country": "China",
        "city": "Shanghai"
    }

def test_clean_text(processor):
    raw = "  This   is \n a <b>test</b>.  "
    cleaned = processor.clean_text(raw)
    assert cleaned == "This is a test."

def test_normalize_date_valid(processor):
    assert processor.normalize_date("2023-10-25 14:30:00") == "2023-10-25T14:30:00"
    assert processor.normalize_date("October 25, 2023") == "2023-10-25T00:00:00"

def test_normalize_date_invalid(processor):
    with pytest.raises(ValueError):
        processor.normalize_date("invalid_date")

def test_extract_entities_fallback(processor):
    # Testing fallback mechanisms if spacy misses something or isn't loaded
    text = "The automotive industry in Shanghai relies heavily on the Port of Shanghai."
    entities = processor.extract_entities(text)
    
    # Check dictionaries fallback
    assert entities.port == "Shanghai"
    assert entities.industry == "Automotive"

def test_process_article_success(processor, valid_raw_article):
    processed = processor.process_article(valid_raw_article)
    
    assert isinstance(processed, ProcessedArticle)
    assert processed.title == "Major Delay at Port of Shanghai"
    assert processed.content == "The Port of Shanghai is facing delays due to weather. Supply chains in the automotive industry are affected."
    assert processed.published_date == "2023-10-25T14:30:00"
    assert processed.country == "China"
    assert processed.city == "Shanghai"
    assert processed.port == "Shanghai" # From entity extraction
    assert processed.industry == "Automotive" # From entity extraction
    assert processed.id is not None
    assert processed.processed_timestamp is not None

def test_process_article_missing_required_fields(processor):
    invalid_raw = {
        "title": "Some Title",
        "content": "Some Content",
        # Missing source, date, url
    }
    with pytest.raises(DataValidationError) as exc_info:
        processor.process_article(invalid_raw)
    assert "Invalid article data" in str(exc_info.value)

def test_process_article_empty_values(processor):
    invalid_raw = {
        "title": "   ", # empty
        "content": "Content",
        "source": "Source",
        "published_date": "2023-10-25",
        "url": "http://test.com"
    }
    with pytest.raises(DataValidationError):
        processor.process_article(invalid_raw)

def test_duplicate_detection_url(processor, valid_raw_article):
    processed1 = processor.process_article(valid_raw_article)
    
    # Same URL, different title
    raw2 = valid_raw_article.copy()
    raw2["title"] = "Different Title"
    
    # Simulate partial processing to get a ProcessedArticle object for testing
    processed2 = processor.process_article(raw2)
    # processed2 will have a different ID because of different title, but same URL
    
    assert processor.is_duplicate(processed2, [processed1]) is True

def test_duplicate_detection_title_similarity(processor, valid_raw_article):
    processed1 = processor.process_article(valid_raw_article)
    
    # Slightly changed title, different URL
    raw2 = valid_raw_article.copy()
    raw2["title"] = "Major Delays at Port of Shanghai" # 'Delay' -> 'Delays'
    raw2["url"] = "https://example.com/news/124"
    processed2 = processor.process_article(raw2)
    
    assert processor.is_duplicate(processed2, [processed1]) is True

def test_duplicate_detection_not_duplicate(processor, valid_raw_article):
    processed1 = processor.process_article(valid_raw_article)
    
    raw2 = {
        "title": "Completely Different News About Something Else",
        "content": "Some other content entirely unrelated to the first one.",
        "source": "Other News",
        "published_date": "2023-11-01",
        "url": "https://example.com/news/999"
    }
    processed2 = processor.process_article(raw2)
    
    assert processor.is_duplicate(processed2, [processed1]) is False
