"""Module containing config data."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Class containing the settings for the application."""

    DATABASE_URL: str = "sqlite:///./backend/db/book_exchange.db"
    SECRET_KEY: str = "16f6efb664f787df222c9657fc275047d2656a4b866396bdeb351aab838b8608"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
