from pydantic import BaseModel, Field

from ..configuration import Configuration


class ConfigurationMessageSchema(BaseModel):
    equipment_id: str = Field(alias="equipmentId")
    task_id: str = Field(alias="taskId")
    configuration: Configuration
