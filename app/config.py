from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Kept server-side only; it must never be exposed to the React frontend.
    groq_api_key: str
    groq_model: str = "openai/gpt-oss-20b"
    allowed_origins: str = "http://localhost:5173,https://portfolio-two-wheat-79.vercel.app"
    resume_path: str = "resume.txt"
    # Keep only recent context. This is enough for follow-up questions and
    # substantially reduces the prompt sent to Groq on every request.
    max_messages: int = 4
    max_message_length: int = 2000
    requests_per_minute: int = 20
    heartbeat_url: str | None = None
    heartbeat_interval_seconds: int = 120

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
