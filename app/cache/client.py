import logging

from app.cache.custom_redis import CustomRedis

logger = logging.getLogger(__name__)


class RedisClient:
    """Класс для управления подключением к Redis с поддержкой явного и автоматического управления."""

    def __init__(
        self,
        host: str,
        port: int,
        ssl_flag: bool,
    ):
        self.host = host
        self.port = port
        self.ssl_flag = ssl_flag
        self._client = None

    async def connect(self):
        """Создает и сохраняет подключение к Redis."""
        if self._client is None:
            try:
                self._client = CustomRedis(
                    host=self.host,
                    port=self.port,
                    ssl=self.ssl_flag,
                    retry_on_timeout=True,
                    health_check_interval=30,
                    decode_responses=True,
                )
                # Проверяем подключение
                await self._client.ping()
            except Exception as e:
                logger.error(f"Ошибка подключения к Redis: {e}")
                raise

    async def close(self):
        """Закрывает подключение к Redis."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def get_client(self) -> CustomRedis:
        """Возвращает объект клиента Redis."""
        if self._client is None:
            raise RuntimeError("Redis клиент не инициализирован. Проверьте lifespan.")
        return self._client

    async def __aenter__(self):
        """Поддерживает асинхронный контекстный менеджер."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Автоматически закрывает подключение при выходе из контекста."""
        await self.close()
