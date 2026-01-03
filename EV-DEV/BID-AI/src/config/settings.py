"""
Configuration settings for BID-AI
Loads from environment variables and provides typed configuration objects
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator

# Load environment variables from .env file
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent


class DatabaseConfig(BaseModel):
    """Database configuration"""

    url: str = Field(default="postgresql://localhost/bidai")
    echo: bool = Field(default=False)
    pool_size: int = Field(default=10)
    max_overflow: int = Field(default=20)

    @classmethod
    def from_env(cls):
        return cls(
            url=os.getenv("DATABASE_URL", "postgresql://localhost/bidai"),
            echo=os.getenv("SQL_ECHO", "False").lower() == "true",
        )


class GoogleCalendarConfig(BaseModel):
    """Google Calendar API configuration"""

    credentials_path: Optional[Path] = None
    token_path: Optional[Path] = None
    enabled: bool = Field(default=False)

    @classmethod
    def from_env(cls):
        creds = os.getenv("GOOGLE_CALENDAR_CREDENTIALS_PATH")
        token = os.getenv("GOOGLE_CALENDAR_TOKEN_PATH")

        return cls(
            credentials_path=Path(creds) if creds else None,
            token_path=Path(token) if token else None,
            enabled=bool(creds and token),
        )


class AIConfig(BaseModel):
    """AI/LLM API configuration"""

    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    @classmethod
    def from_env(cls):
        return cls(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )


class ScraperConfig(BaseModel):
    """Web scraper configuration"""

    user_agent: str = Field(default="BID-AI/1.0")
    rate_limit_seconds: float = Field(default=2.0)
    timeout_seconds: int = Field(default=30)

    # Portal credentials
    bcbid_username: Optional[str] = None
    bcbid_password: Optional[str] = None
    merx_username: Optional[str] = None
    merx_password: Optional[str] = None

    @classmethod
    def from_env(cls):
        return cls(
            user_agent=os.getenv("SCRAPER_USER_AGENT", "BID-AI/1.0"),
            rate_limit_seconds=float(os.getenv("SCRAPER_RATE_LIMIT_SECONDS", "2")),
            timeout_seconds=int(os.getenv("SCRAPER_TIMEOUT_SECONDS", "30")),
            bcbid_username=os.getenv("BCBID_USERNAME"),
            bcbid_password=os.getenv("BCBID_PASSWORD"),
            merx_username=os.getenv("MERX_USERNAME"),
            merx_password=os.getenv("MERX_PASSWORD"),
        )


class EmailConfig(BaseModel):
    """Email notification configuration"""

    smtp_host: str = Field(default="smtp.gmail.com")
    smtp_port: int = Field(default=587)
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    notification_email_to: Optional[str] = None
    enabled: bool = Field(default=False)

    @classmethod
    def from_env(cls):
        smtp_user = os.getenv("SMTP_USERNAME")
        smtp_pass = os.getenv("SMTP_PASSWORD")

        return cls(
            smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_username=smtp_user,
            smtp_password=smtp_pass,
            notification_email_to=os.getenv("NOTIFICATION_EMAIL_TO"),
            enabled=bool(smtp_user and smtp_pass),
        )


class LoggingConfig(BaseModel):
    """Logging configuration"""

    level: str = Field(default="INFO")
    file_path: Path = Field(default=PROJECT_ROOT / "logs" / "bidai.log")

    @classmethod
    def from_env(cls):
        return cls(
            level=os.getenv("LOG_LEVEL", "INFO"),
            file_path=Path(
                os.getenv("LOG_FILE_PATH", str(PROJECT_ROOT / "logs" / "bidai.log"))
            ),
        )


class SystemConfig(BaseModel):
    """System-wide configuration"""

    timezone: str = Field(default="America/Vancouver")
    environment: str = Field(default="development")

    @classmethod
    def from_env(cls):
        return cls(
            timezone=os.getenv("TIMEZONE", "America/Vancouver"),
            environment=os.getenv("ENVIRONMENT", "development"),
        )


class Settings(BaseModel):
    """Master settings object"""

    database: DatabaseConfig
    google_calendar: GoogleCalendarConfig
    ai: AIConfig
    scraper: ScraperConfig
    email: EmailConfig
    logging: LoggingConfig
    system: SystemConfig

    @classmethod
    def load(cls):
        """Load all settings from environment"""
        return cls(
            database=DatabaseConfig.from_env(),
            google_calendar=GoogleCalendarConfig.from_env(),
            ai=AIConfig.from_env(),
            scraper=ScraperConfig.from_env(),
            email=EmailConfig.from_env(),
            logging=LoggingConfig.from_env(),
            system=SystemConfig.from_env(),
        )

    def validate_required(self):
        """Validate that required settings are present"""
        errors = []

        # Check database
        if not self.database.url:
            errors.append("DATABASE_URL is required")

        # Warn about optional features
        if not self.google_calendar.enabled:
            print("⚠️  Google Calendar integration not configured")

        if not self.ai.anthropic_api_key and not self.ai.openai_api_key:
            print("⚠️  No AI API keys configured (Anthropic or OpenAI)")

        if not self.email.enabled:
            print("⚠️  Email notifications not configured")

        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global settings instance (singleton pattern)

    Returns:
        Settings object
    """
    global _settings

    if _settings is None:
        _settings = Settings.load()
        _settings.validate_required()

    return _settings


# Convenience exports
settings = get_settings()


if __name__ == "__main__":
    # Test configuration loading
    print("Loading BID-AI configuration...")
    print(f"\nDatabase URL: {settings.database.url}")
    print(f"Environment: {settings.system.environment}")
    print(f"Log Level: {settings.logging.level}")
    print(
        f"Google Calendar: {'✓ Enabled' if settings.google_calendar.enabled else '✗ Disabled'}"
    )
    print(
        f"Email Notifications: {'✓ Enabled' if settings.email.enabled else '✗ Disabled'}"
    )
    print(
        f"Anthropic API: {'✓ Configured' if settings.ai.anthropic_api_key else '✗ Not configured'}"
    )
    print(
        f"OpenAI API: {'✓ Configured' if settings.ai.openai_api_key else '✗ Not configured'}"
    )
    print("\n✓ Configuration loaded successfully!")
