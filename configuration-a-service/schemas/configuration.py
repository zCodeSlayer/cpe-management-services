from pydantic import BaseModel, Field


class ConfigurationParameters(BaseModel):
    username: str
    password: str
    vlan: int | None = Field(default=None)
    interfaces: list[int] = Field(default_factory=list)


class Configuration(BaseModel):
    timeout_in_seconds: int = Field(alias="timeoutInSeconds")
    parameters: list[ConfigurationParameters] = Field(default_factory=list)
