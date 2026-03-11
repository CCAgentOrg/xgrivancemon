"""Configuration management for XGrivanceMon"""
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    x_api_key: str = ""
    x_api_secret: str = ""
    
    # Database
    turso_url: str = ""
    turso_token: str = ""
    
    # Scheduling
    collection_hour: int = 8
    collection_minute: int = 0
    report_day: str = "sun"  # Sunday
    report_hour: int = 10
    
    # App Settings
    debug: bool = False
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
