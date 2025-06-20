"""
Конфигурации
"""
from typing import Optional
from pydantic_settings import BaseSettings


class LLMConfig(BaseSettings):
    api_key: str
    base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-chat"
    temperature: float = 0.3
    max_tokens: int = 4096


class Settings(BaseSettings):
    """Настройки приложения"""

    # API-агенты
    llm_base: LLMConfig
    llm_tree: Optional[LLMConfig] = None
    llm_content: Optional[LLMConfig] = None
    llm_validator: Optional[LLMConfig] = None
    llm_regenerator: Optional[LLMConfig] = None
    
    # Валидация
    max_self_review_iterations: int = 2
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = '__'


settings = Settings()
