import asyncio
import redis.asyncio as redis
from typing import Optional

from config.redis_settings import redis_settings


class RedisService:
    def __init__(self):
        self.redis: Optional[redis.Redis] = None

    async def init(self):
        self.redis = await redis.from_url(
            url=f"redis://{redis_settings.host}:{redis_settings.port}",
            encoding="utf8",
            decode_responses=True
        )

    async def close(self):
        await self.redis.close()

    async def set(self, key: str, value: any, ex: int = None):
        if ex:
            await self.redis.set(key, value, ex=ex)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def exists(self, key: str):
        return await self.redis.exists(key)

    async def set_with_ttl(self, key: str, value: any, ttl: int):
        await self.redis.set(key, value, ex=ttl)


redis_service = RedisService()