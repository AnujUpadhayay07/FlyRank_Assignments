from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Embeddable Widget & Lead-Capture Platform"
    database_url: str = "sqlite:///./data/widget_platform.db"
    secret_key: str = "change-this-secret-key"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()