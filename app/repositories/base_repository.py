from typing import Type, TypeVar, Generic, Optional
import logging
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
        res = await self.session.execute(select(self.model).filter(self.model.id == id))
        return res.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[T]:
        res = await self.session.execute(
            select(self.model).filter(self.model.name == name)
        )
        return res.scalar_one_or_none()

    async def create(self, data: dict) -> T:
        value = self.model(**data)
        self.session.add(value)
        await self.session.flush()
        return value

    async def update(self, data: dict, update_data: dict) -> T:
        for key, value in update_data.items():
            setattr(data, key, value)
            await self.session.flush()
        return data

    async def delete(self, id: int) -> int:
        query = delete(self.model).filter(self.model.id == id)
        await self.session.execute(query)
        await self.session.flush()
 