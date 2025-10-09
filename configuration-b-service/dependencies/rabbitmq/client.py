import asyncio
from typing import AsyncGenerator, Any

from .rabbitmq_service import RabbitMQService
from config import Settings

settings = Settings()


async def get_rabbitmq_connection() -> AsyncGenerator[RabbitMQService, Any]:
    async with RabbitMQService(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_login,
        password=settings.rabbitmq_password
    ) as service:
        yield service
