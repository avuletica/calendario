import os
from typing import Any, Dict, Optional

from pydantic import BaseSettings, EmailStr, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SECRET_KEY")
    # 60 minutes * 24 hours * 7 days = 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # uvicorn
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8080"))
    DEBUG: bool = bool(os.getenv("DEBUG", "0"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    PROJECT_NAME: str = "calendario"

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "calendario_db_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "calendario_db_password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "calendario_db")
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL",
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}",
    )

    # Here only because of tests and faster demo.
    FIRST_USER_EMAIL: EmailStr = "john@doe.com"
    FIRST_USER_PASSWORD: str = "password"

    class Config:
        case_sensitive = True


settings = Settings()
