import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables or .env file.
    """
    # Application settings
    APP_NAME: str = "Infotact-Disruption-Monitor"
    APP_VERSION: str = "1.0.0"
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Data processing settings
    SIMILARITY_THRESHOLD: float = 0.85
    SPACY_MODEL: str = "en_core_web_sm"

    # Pydantic Settings configuration to load from .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate a global settings object to be imported by other modules
settings = Settings()
