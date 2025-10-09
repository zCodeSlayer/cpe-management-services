from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_host: str
    app_port: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class RedisSettings(BaseSettings):
    redis_host: str
    redis_port: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class RabbitMQSettings(BaseSettings):
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_login: str
    rabbitmq_password: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class Settings(AppSettings, RedisSettings, RabbitMQSettings):
    pass
