from typing import TypeVar, Type
import logging
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import select, delete
from sqlalchemy.orm import DeclarativeBase


TModel = TypeVar("TModel", bound=DeclarativeBase)

logger = logging.getLogger(__name__)


class AbstractRepository(ABC):
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_one_or_none_by_id(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def create(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update(self, filter_by: int | str, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, delete_all: bool, filter_by: dict):
        raise NotImplementedError


class BaseRepository(AbstractRepository):
    model: Type[TModel] = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        res = await self.session.execute(select(self.model))
        return res.scalars().all()

    async def get_one_or_none_by_id(self, id: int):
        res = await self.session.execute(select(self.model).where(self.model.id == id))
        return res.scalar_one_or_none()

    async def create(self, data: dict):
        value = self.model(**data)
        self.session.add(value)
        try:
            await self.session.commit()
            await self.session.refresh(value)
        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"Failed to create record:{str(e)}")
            raise 
        return value

    async def update(self, obj: dict, update_data: dict) -> dict:
        for key, value in update_data.items():
            setattr(obj, key, value)
        try:
            await self.session.commit()
            await self.session.refresh(obj)
        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"Failed to update data:{str(e)}")
            raise 
        return obj

    async def delete(self, id: int | None, delete_all: bool = False) -> int:
        query = delete(self.model)
        if not delete_all:
            query = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error("Failed to delete data")
            raise 
        return result.rowcount
