import pytest
import json
from src.data_processor import ProcessedArticle
from src.output_formatter import OutputFormatter

@pytest.fixture
def mock_processed_article():
    return ProcessedArticle(
        id="123456",
        title="Test Title",
        content="Test Content",
        source="Test Source",
        published_date="2023-10-25T14:30:00",
        url="https://test.com",
        country="US",
        industry="Tech",
        processed_timestamp="2023-10-25T15:00:00Z"
    )

def test_format_to_dict(mock_processed_article):
    result = OutputFormatter.format_to_dict(mock_processed_article)
    
    assert isinstance(result, dict)
    assert result["article_id"] == "123456"
    assert result["title"] == "Test Title"
    assert result["entities"]["country"] == "US"
    assert result["entities"]["industry"] == "Tech"
    assert result["entities"]["port"] is None
    assert result["metadata"]["language"] == "en"

def test_format_to_json_pretty(mock_processed_article):
    result = OutputFormatter.format_to_json(mock_processed_article, pretty=True)
    
    assert isinstance(result, str)
    assert "\n" in result
    assert "    " in result # Check for indentation
    
    # Verify it can be parsed back
    parsed = json.loads(result)
    assert parsed["article_id"] == "123456"

def test_format_to_json_compact(mock_processed_article):
    result = OutputFormatter.format_to_json(mock_processed_article, pretty=False)
    
    assert isinstance(result, str)
    assert "\n" not in result
    assert '": ' not in result # Check for compact separators
    assert '", "' not in result
    
    parsed = json.loads(result)
    assert parsed["article_id"] == "123456"

def test_format_batch(mock_processed_article):
    batch = [mock_processed_article, mock_processed_article]
    
    result_list = OutputFormatter.format_batch(batch, as_json=False)
    assert isinstance(result_list, list)
    assert len(result_list) == 2
    assert result_list[0]["article_id"] == "123456"
    
    result_json = OutputFormatter.format_batch(batch, as_json=True, pretty=False)
    assert isinstance(result_json, str)
    assert result_json.startswith("[")
    assert result_json.endswith("]")
    
    parsed = json.loads(result_json)
    assert len(parsed) == 2
