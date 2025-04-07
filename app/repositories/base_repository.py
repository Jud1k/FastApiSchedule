from typing import Type, TypeVar, Generic
import logging
from abc import ABC, abstractmethod
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import delete
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import Base

logger = logging.getLogger(__name__)


T = TypeVar("T", bound=Base)


class SqlAlchemyRepository(Generic[T]):
    model: Type[T] = None
    async def get_all(self, session: AsyncSession) -> list[T]:
        stmt = select(self.model)
        res = await session.execute(stmt)
        return res.scalars().all()

    async def get_one_or_none_by_id(
        self, session: AsyncSession, id: int
    ) -> dict | None:
        res = await session.execute(select(self.model).filter(self.model.id == id))
        return res.scalar_one_or_none()

    async def create(self, session: AsyncSession, data: dict) -> dict:
        try:
            value = self.model(**data)
            session.add(value)
            await session.flush()
        except IntegrityError as e:
            logger.error(f"Failed to create record:{str(e)}")
            raise
        return value

    async def update(self, session: AsyncSession, obj: dict, update_data: dict) -> dict:
        try:
            for key, value in update_data.items():
                setattr(obj, key, value)
                await session.flush()
        except IntegrityError as e:
            logger.error(f"Failed to update data:{str(e)}")
            raise
        return obj

    async def delete(
        self, session: AsyncSession, id: int | None, delete_all: bool = False
    ) -> int:
        try:
            query = delete(self.model)
            if not delete_all:
                query = delete(self.model).filter(self.model.id == id)
            result = await session.execute(query)
            await session.flush()
        except SQLAlchemyError as e:
            logger.error("Failed to delete data")
            raise
        return result.rowcount
