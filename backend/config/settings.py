"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os


class Settings(BaseSettings):
    """Pydantic Settings — loads from .env file automatically."""

    # Application
    app_name: str = Field(default="IntelliPlant", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=True, alias="DEBUG")
    cors_origins: str = Field(
        default="http://localhost:5173", alias="CORS_ORIGINS"
    )

    # LLM
    google_api_key: str = Field(default="", alias="GOOGLE_API_KEY")

    # Neo4j
    neo4j_uri: str = Field(default="bolt://localhost:7687", alias="NEO4J_URI")
    neo4j_user: str = Field(default="neo4j", alias="NEO4J_USER")
    neo4j_password: str = Field(
        default="intelliplant2026", alias="NEO4J_PASSWORD"
    )

    # Storage
    upload_dir: str = Field(default="./uploads", alias="UPLOAD_DIR")
    chroma_persist_dir: str = Field(
        default="./chroma_db", alias="CHROMA_PERSIST_DIR"
    )
    sqlite_url: str = Field(
        default="sqlite+aiosqlite:///./intelliplant.db", alias="SQLITE_URL"
    )

    # Models
    llm_model: str = "gemini-2.0-flash"
    embedding_model: str = "all-MiniLM-L6-v2"
    spacy_model: str = "en_core_web_sm"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


# Singleton instance
settings = Settings()
