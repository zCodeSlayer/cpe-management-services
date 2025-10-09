from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQSettings(BaseSettings):
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_login: str
    rabbitmq_password: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class ConfigurationAServiceSettings(BaseSettings):
    configuration_a_service_url: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class Settings(RabbitMQSettings, ConfigurationAServiceSettings):
    pass
