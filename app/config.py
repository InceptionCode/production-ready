from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "./data/tasks.db"
    log_level: str = "INFO"
    port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
