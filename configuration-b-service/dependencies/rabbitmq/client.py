import asyncio
from typing import AsyncGenerator, Any

from .rabbitmq_service import RabbitMQService


async def get_rabbitmq_connection() -> AsyncGenerator[RabbitMQService, Any]:
    async with RabbitMQService() as service:
        yield service
