from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    assistant_stage: str = "basic"
    demo_mode: bool = True
    llm_api_key: str = ""
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4.1-mini"
    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 256
    qdrant_url: str = "http://qdrant:6333"
    collection_name: str = "engineering-careers"
    knowledge_path: Path = Path("/knowledge")
    top_k: int = 5
    chunk_size: int = 900
    chunk_overlap: int = 120
    # Support both Docker's /app working directory and local runs from backend/.
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
