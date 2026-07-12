import json
from typing import List, Dict, Any, Union

from src.data_processor import ProcessedArticle
from src.utils.logger import get_logger

logger = get_logger(__name__)

class OutputFormatter:
    """
    Handles the formatting of ProcessedArticle objects into standardized
    dictionaries or JSON strings for downstream ingestion (e.g., LLM Classification,
    Knowledge Graphs).
    """

    @staticmethod
    def format_to_dict(article: ProcessedArticle) -> Dict[str, Any]:
        """
        Converts a ProcessedArticle into the standardized dictionary format.
        """
        try:
            formatted_dict = {
                "article_id": article.id,
                "title": article.title,
                "source": article.source,
                "published_date": article.published_date,
                "entities": {
                    "country": article.country,
                    "city": article.city,
                    "port": article.port,
                    "supplier_location": article.supplier_location,
                    "industry": article.industry
                },
                "content": article.content,
                "metadata": {
                    "language": article.language,
                    "processed_timestamp": article.processed_timestamp,
                    "version": article.metadata.get("version", "1.0")
                }
            }
            logger.debug(f"Successfully formatted article {article.id} to dict.")
            return formatted_dict
        except Exception as e:
            logger.error(f"Failed to format article to dict: {e}")
            raise

    @staticmethod
    def format_to_json(article: ProcessedArticle, pretty: bool = False) -> str:
        """
        Converts a ProcessedArticle into a JSON string.
        
        Args:
            article: The ProcessedArticle to format.
            pretty: If True, returns a nicely indented JSON string.
                    If False, returns a compact JSON string.
        """
        formatted_dict = OutputFormatter.format_to_dict(article)
        
        if pretty:
            return json.dumps(formatted_dict, indent=4, ensure_ascii=False)
        else:
            return json.dumps(formatted_dict, separators=(',', ':'), ensure_ascii=False)

    @staticmethod
    def format_batch(articles: List[ProcessedArticle], as_json: bool = False, pretty: bool = False) -> Union[List[Dict[str, Any]], str]:
        """
        Formats a batch of ProcessedArticle objects.
        
        Args:
            articles: List of ProcessedArticle objects.
            as_json: If True, returns a single JSON string representing the list.
            pretty: If True and as_json is True, formats the JSON with indents.
            
        Returns:
            A list of dictionaries or a JSON string.
        """
        logger.info(f"Formatting batch of {len(articles)} articles.")
        
        formatted_list = [OutputFormatter.format_to_dict(article) for article in articles]
        
        if as_json:
            if pretty:
                return json.dumps(formatted_list, indent=4, ensure_ascii=False)
            else:
                return json.dumps(formatted_list, separators=(',', ':'), ensure_ascii=False)
        
        return formatted_list
