from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    
    DATABASE_URL: str = "sqlite:///../database-scripts/recomienda_app.db"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "eilaeila55314")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Recomienda App")
    
    FOURSQUARE_API_KEY: str = os.getenv("FOURSQUARE_API_KEY", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
