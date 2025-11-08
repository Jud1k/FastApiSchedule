from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    REDIS_PORT: int
    REDIS_SSL: bool
    REDIS_HOST: str
    SECRET_KEY: str
    ALGORITHM: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Setting()


def get_db_url() -> str:
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
