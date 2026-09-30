from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FitBuddy - AI Fitness Plan Generator"

    gemini_api_key: str = ""

    gemini_workout_model: str = "gemini-2.5-flash"
    gemini_tip_model: str = "gemini-2.5-flash"
    gemini_update_model: str = "gemini-2.5-flash"

    database_url: str = "sqlite:///./fitbuddy.db"

    admin_password: str = "admin123"

    ai_demo_mode: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()