from datetime import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, Integer, Text, func
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.core.config import get_db_url

DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

int_pk = Annotated[int, mapped_column(Integer,primary_key=True, autoincrement="auto")]
created_at = Annotated[datetime, mapped_column(TIMESTAMP, server_default=func.now())]
updated_at = Annotated[
    datetime, mapped_column(TIMESTAMP, server_default=func.now(), onupdate=datetime.now)
]
uniq_str = Annotated[str, mapped_column(Text,unique=True, nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def to_dict(self) -> dict:
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            # Автоматически преобразуем datetime в строку
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result
