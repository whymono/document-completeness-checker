from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import List

class Settings(BaseSettings):
    FRONTEND_URLS: str = "http://localhost:5173"
    GEMINI_API_KEY: str

    @property
    def cors_origins(self) -> List[str]:
        return [url.strip() for url in self.FRONTEND_URLS.split(",")]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
