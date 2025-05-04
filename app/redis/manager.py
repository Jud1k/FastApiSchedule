import logging
from functools import wraps
from typing import Callable, Awaitable, Any
from fastapi import Depends
from app.core.config import settings
from app.redis.redis_client import RedisClient
from redis.asyncio import Redis
logger = logging.getLogger(__name__)

redis_manager = RedisClient(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    ssl_flag=settings.REDIS_SSL,
)


async def get_redis() -> Redis:
    """Функция зависимости для получения клиента Redis"""
    return redis_manager.get_client()

