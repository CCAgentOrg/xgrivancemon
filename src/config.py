"""Configuration settings using Pydantic"""
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # TursoDB Configuration
    turso_database_url: str = Field(default="libsql://xgrivancemon.turso.io")
    turso_auth_token: str = Field(default="")
    
    # X Cookie-Based Authentication (NOT API)
    x_auth_token: str = Field(default="", description="X auth_token cookie from browser session")
    x_csrf_token: str = Field(default="", description="X ct0 cookie (CSRF token)")
    
    # Collection Settings
    default_collection_window_hours: int = Field(default=168)  # 7 days
    rate_limit_delay_seconds: int = Field(default=60)
    max_requests_per_session: int = Field(default=100)
    
    # Application Settings
    app_name: str = Field(default="XGrivanceMon")
    debug: bool = Field(default=False)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
