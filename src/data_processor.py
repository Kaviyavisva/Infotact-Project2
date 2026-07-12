import re
import hashlib
import unicodedata
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, Tuple
from dateutil import parser as date_parser
import spacy
from pydantic import BaseModel, Field, HttpUrl, ValidationError, field_validator
from difflib import SequenceMatcher

from src.utils.logger import get_logger
from src.utils.config import settings

logger = get_logger(__name__)

class DataValidationError(Exception):
    """Custom exception for data validation errors."""
    pass

class Entities(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    port: Optional[str] = None
    supplier_location: Optional[str] = None
    industry: Optional[str] = None

class ProcessedArticle(BaseModel):
    id: str
    title: str
    content: str
    summary: Optional[str] = None
    source: str
    author: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    port: Optional[str] = None
    supplier_location: Optional[str] = None
    industry: Optional[str] = None
    published_date: str
    url: str
    language: str = "en"
    processed_timestamp: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RawArticle(BaseModel):
    """Schema for validating incoming raw data."""
    title: str
    content: str
    source: str
    published_date: str
    url: str
    author: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    port: Optional[str] = None
    supplier_location: Optional[str] = None
    industry: Optional[str] = None

    @field_validator('title', 'content', 'source', 'url', mode='before')
    def check_not_empty(cls, v, info):
        if not v or not str(v).strip():
            raise ValueError(f"{info.field_name} cannot be empty or null.")
        return v

class DataProcessor:
    """
    Handles data cleaning, validation, entity extraction, and duplicate detection
    for logistics and supply chain news articles.
    """
    def __init__(self):
        try:
            # Load spaCy model for entity extraction
            self.nlp = spacy.load(settings.SPACY_MODEL)
            logger.info(f"Successfully loaded spaCy model: {settings.SPACY_MODEL}")
        except OSError:
            logger.warning(f"spaCy model '{settings.SPACY_MODEL}' not found. "
                           f"Run 'python -m spacy download {settings.SPACY_MODEL}' to install. "
                           "Falling back to regex/dictionary extraction where possible.")
            self.nlp = None

        # Basic dictionaries for fallback extraction
        self.known_ports = {"shanghai", "singapore", "los angeles", "rotterdam", "hamburg", "antwerp", "new york"}
        self.known_industries = {"semiconductor", "automotive", "pharmaceutical", "agriculture", "electronics", "retail"}

    def clean_text(self, text: str) -> str:
        """
        Removes HTML tags, extra spaces, unwanted newlines, invalid unicode, 
        and normalizes punctuation.
        """
        if not text:
            return ""
        
        # 1. Remove HTML tags
        text = re.sub(r'<[^>]+>', '', str(text))
        
        # 2. Normalize unicode (fixes invalid unicode characters)
        text = unicodedata.normalize('NFKC', text)
        
        # 3. Remove unwanted newlines and carriage returns
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        # 4. Normalize punctuation (e.g., smart quotes to straight quotes)
        text = text.translate(str.maketrans('“”‘’', '""\'\''))
        
        # 5. Remove duplicate whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def normalize_date(self, date_str: str) -> str:
        """
        Converts various date strings into standard ISO format (YYYY-MM-DDTHH:MM:SSZ).
        Raises ValueError if invalid.
        """
        if not date_str:
            raise ValueError("Empty date string provided.")
        
        try:
            dt = date_parser.parse(date_str)
            return dt.isoformat()
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid date format '{date_str}': {e}")

    def generate_id(self, url: str, title: str) -> str:
        """Generates a unique ID based on URL and Title."""
        unique_string = f"{url}-{title}".encode('utf-8')
        return hashlib.sha256(unique_string).hexdigest()

    def extract_entities(self, text: str) -> Entities:
        """
        Extracts entities using spaCy with regex/dictionary fallbacks.
        """
        entities = Entities()
        if not text:
            return entities

        if self.nlp:
            doc = self.nlp(text)
            
            for ent in doc.ents:
                if ent.label_ == "GPE": # Geo-Political Entity
                    if not entities.country:
                        # Simplification: Assign first GPE to country/city loosely
                        entities.country = ent.text
                    elif not entities.city:
                        entities.city = ent.text
                elif ent.label_ == "ORG":
                    if not entities.supplier_location:
                        entities.supplier_location = ent.text

        # Fallback/Enhancement using dictionaries & regex
        lower_text = text.lower()
        
        # Find ports
        if not entities.port:
            for port in self.known_ports:
                if port in lower_text:
                    entities.port = port.title()
                    break
                    
        # Find industry
        if not entities.industry:
            for industry in self.known_industries:
                if industry in lower_text:
                    entities.industry = industry.title()
                    break

        return entities

    def is_duplicate(self, new_article: ProcessedArticle, existing_articles: List[ProcessedArticle]) -> bool:
        """
        Checks if the new_article is a duplicate against a list of existing articles based on:
        1. Exact URL match
        2. ID hash match
        3. Title similarity > threshold
        4. Content similarity > threshold
        """
        threshold = settings.SIMILARITY_THRESHOLD
        
        for existing in existing_articles:
            # 1. URL Match
            if new_article.url == existing.url:
                logger.debug(f"Duplicate found by URL: {new_article.url}")
                return True
                
            # 2. Hash Match
            if new_article.id == existing.id:
                logger.debug(f"Duplicate found by ID hash: {new_article.id}")
                return True
                
            # 3. Title Similarity
            title_sim = SequenceMatcher(None, new_article.title, existing.title).ratio()
            if title_sim >= threshold:
                logger.debug(f"Duplicate found by Title similarity ({title_sim:.2f})")
                return True
                
            # 4. Content Similarity
            content_sim = SequenceMatcher(None, new_article.content, existing.content).ratio()
            if content_sim >= threshold:
                logger.debug(f"Duplicate found by Content similarity ({content_sim:.2f})")
                return True
                
        return False

    def process_article(self, raw_data: Dict[str, Any]) -> ProcessedArticle:
        """
        Orchestrates the entire cleaning, validation, and extraction pipeline.
        Returns a ProcessedArticle object.
        Raises DataValidationError on failure.
        """
        if not isinstance(raw_data, dict):
            logger.error("Input data is not a dictionary.")
            raise DataValidationError("Input data must be a dictionary.")

        # 1. Validation (Structure and required fields)
        try:
            raw_article = RawArticle(**raw_data)
        except ValidationError as e:
            logger.error(f"Validation failed for article: {e.errors()}")
            raise DataValidationError(f"Invalid article data: {e.errors()}")

        # 2. Cleaning
        cleaned_title = self.clean_text(raw_article.title)
        cleaned_content = self.clean_text(raw_article.content)
        cleaned_source = self.clean_text(raw_article.source)
        cleaned_url = raw_article.url.strip()
        
        try:
            iso_date = self.normalize_date(raw_article.published_date)
        except ValueError as e:
            logger.error(f"Date parsing failed: {e}")
            raise DataValidationError(str(e))

        # 3. Entity Extraction
        entities = self.extract_entities(cleaned_content)
        
        # Override extracted with provided if they exist in raw_data
        country = self.clean_text(raw_article.country) if raw_article.country else entities.country
        city = self.clean_text(raw_article.city) if raw_article.city else entities.city
        port = self.clean_text(raw_article.port) if raw_article.port else entities.port
        supplier_loc = self.clean_text(raw_article.supplier_location) if raw_article.supplier_location else entities.supplier_location
        industry = self.clean_text(raw_article.industry) if raw_article.industry else entities.industry
        author = self.clean_text(raw_article.author) if raw_article.author else None

        # 4. Generate ID
        article_id = self.generate_id(cleaned_url, cleaned_title)

        # 5. Build Processed Object
        processed_timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        try:
            processed = ProcessedArticle(
                id=article_id,
                title=cleaned_title,
                content=cleaned_content,
                summary=None, # TBD by LLM in next pipeline stage
                source=cleaned_source,
                author=author,
                country=country,
                city=city,
                port=port,
                supplier_location=supplier_loc,
                industry=industry,
                published_date=iso_date,
                url=cleaned_url,
                processed_timestamp=processed_timestamp,
                metadata={"version": settings.APP_VERSION}
            )
            logger.info(f"Successfully processed article: {article_id}")
            return processed
            
        except ValidationError as e:
            logger.error(f"Final model validation failed: {e.errors()}")
            raise DataValidationError(f"Failed to build processed article: {e.errors()}")
