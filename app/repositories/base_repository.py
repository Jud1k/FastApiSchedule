from typing import Type, TypeVar, Generic, Optional
import logging
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import Base

logger = logging.getLogger(__name__)


T = TypeVar("T", bound=Base)


class SqlAlchemyRepository(Generic[T]):
    model: Type[T] = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[T]:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_one_or_none_by_id(self, id: int) -> Optional[T]:
        stmt=select(self.model).filter(self.model.id==id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_one_or_none(self, filters:BaseModel) -> Optional[T]:
        filters_dict=filters.model_dump(exclude_unset=True)
        stmt = select(self.model).filter_by(**filters_dict)
        res = await self.session.execute(stmt)
        record = res.scalar_one_or_none()
        return record
        
    async def create(self, data: dict) -> T:
        value = self.model(**data)
        self.session.add(value)
        await self.session.flush()
        return value

    async def create_many(self, data: list[dict]) -> list[T]:
        values = [self.model(**d) for d in data]
        self.session.add_all(values)
        await self.session.flush()
        return values

    async def update(self, data: dict, update_data: dict) -> T:
        for key, value in update_data.items():
            setattr(data, key, value)
            await self.session.flush()
        return data

    async def delete(self, id: int) -> int:
        stmt = delete(self.model).filter(self.model.id == id)
        await self.session.execute(stmt)
        await self.session.flush()
