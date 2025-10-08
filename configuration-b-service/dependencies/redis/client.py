import asyncio

import redis.asyncio as redis


async def get_redis():
    async with redis.Redis(
        host="localhost", port=6379, decode_responses=True
    ) as client:
        yield client
