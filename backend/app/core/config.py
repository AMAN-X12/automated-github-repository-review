from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = "development"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/ai_pr_reviewer"
    redis_url: str = "redis://localhost:6379/0"

    # Optional until you actually wire up the GitHub App / LLM calls (Phase 1-4).
    # Kept optional so importing this module doesn't crash before those exist.
    github_app_id: str | None = None
    github_private_key: str | None = None
    github_webhook_secret: str | None = None
    llm_api_key: str | None = None
    llm_model: str = ""


settings = Settings()
