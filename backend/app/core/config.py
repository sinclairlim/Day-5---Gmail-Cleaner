from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    REDIRECT_URI: str = "http://localhost:8000/api/auth/callback"

    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"  # Options: gpt-4o-mini, gpt-3.5-turbo, gpt-4

    # App Settings
    SECRET_KEY: str
    CORS_ORIGINS: str = "http://localhost:3000"
    ENVIRONMENT: str = "development"

    # Gmail API Scopes
    GMAIL_SCOPES: List[str] = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid"
    ]

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
