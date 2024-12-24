import os
from dotenv import load_dotenv
load_dotenv()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CLAUDE_API_KEY: str

    ANTHROPIC_LLM_MODEL : str = "claude-3-5-sonnet-20241022"
    ANTHROPIC_LLM_MAX_TOKENS : int = 1024
    ANTHROPIC_LLM_TEMPERATURE : float = 0
    
    ANTHROPIC_VERIFY_URL : str = "https://api.anthropic.com/verify_key"
    ANTHROPIC_GENERATE_URL : str = "https://api.anthropic.com/generate"

    class Config:
        env_file = ".env"
        extra = "ignore"

anthropic_settings = Settings()