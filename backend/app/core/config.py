from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    FRONTEND_URL: str = "http://localhost:5173"
    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
