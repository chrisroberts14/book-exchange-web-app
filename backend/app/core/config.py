"""Module containing config data."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Class containing the settings for the application."""

    DATABASE_URL: str = "sqlite:///./backend/db/book_exchange.db"


settings = Settings()
