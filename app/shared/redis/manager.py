from app.core.config import settings
from app.shared.redis.client import RedisClient
from redis.asyncio import Redis

redis_manager = RedisClient(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    ssl_flag=settings.REDIS_SSL,
)


async def get_redis() -> Redis:
    """Функция зависимости для получения клиента Redis"""
    return redis_manager.get_client()
