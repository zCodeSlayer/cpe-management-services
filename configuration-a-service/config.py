from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_host: str
    app_port: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class Settings(AppSettings):
    pass
