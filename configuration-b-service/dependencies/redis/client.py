import asyncio

import redis.asyncio as redis

from config import Settings

settings = Settings()


async def get_redis():
    async with redis.Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True) as client:
        yield client
