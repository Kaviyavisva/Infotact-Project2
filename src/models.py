"""
models.py

Pydantic models for the Supply Chain Disruption Monitoring project.
"""

from pydantic import BaseModel


class NewsArticle(BaseModel):
    """
    Model representing a fetched news article.
    """
    title: str
    url: str
    snippet: str


class ClassifiedArticle(BaseModel):
    """
    Model representing a classified news article.
    """
    title: str
    category: str
    severity: str
    reason: str