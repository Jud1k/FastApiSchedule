import logging

from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import Base

logger = logging.getLogger(__name__)


T = TypeVar("T", bound=Base)


class SqlAlchemyRepository(Generic[T]):
    model: type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self,skip:int=0,limit:int=100) -> list[T]:
        logger.info(f"Search all records {self.model.__name__}.")
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        records = list(result.scalars().all())
        logger.info(f"Find {len(records)} records.")
        return records
    
    async def get_one_or_none_by_id(self, id: int) -> T | None:
        logger.info(f"Search {self.model.__name__} with ID {id}.")
        stmt = select(self.model).filter(self.model.id == id) # type: ignore
        result = await self.session.execute(stmt)
        record = result.scalar_one_or_none()
        if record:
            logger.info(f"Record with ID {id} find.")
        else:
            logger.info(f"Record with ID {id} does not find.")
        return record 

    async def get_one_or_none(self, filters: BaseModel) -> T | None:
        filters_dict = filters.model_dump(exclude_unset=True)
        logger.info(f"Search {self.model.__name__} with filters: {filters_dict}.")
        stmt = select(self.model).filter_by(**filters_dict)
        result = await self.session.execute(stmt)
        record = result.scalar_one_or_none()
        if record:
            logger.info(f"Record find by filters: {filters_dict}.")
        if not record:
            logger.info(f"Record not find by filters: {filters_dict}.")
        return record
            
    async def create(self, data: BaseModel) -> T:
        logger.info(f"Creating record {self.model.__name__}.")
        data_dict = data.model_dump(exclude_unset=True)
        value = self.model(**data_dict)
        self.session.add(value)
        await self.session.flush()
        logger.info(f"Record {self.model.__name__} successfully created.")
        return value

    async def create_many(self, data: list[BaseModel]) -> list[T]:
        data_list = [record.model_dump(exclude_unset=True) for record in data]
        logger.info(f"Creating records {self.model.__name__}. Count:{len(data_list)}")
        values = [self.model(**item) for item in data_list]
        self.session.add_all(values)
        await self.session.flush()
        logger.info(f"{len(data_list)} records successfully created.")
        return values

    async def update(self, data: T, update_data: BaseModel) -> T:
        data_dict = data.to_dict()
        update_data_dict = update_data.model_dump(exclude_unset=True)
        for field in data_dict:
            if field in update_data_dict:
                setattr(data,field,update_data_dict[field])
        await self.session.flush()
        logger.info(f"Record {self.model.__name__} successfully updated.")
        return data

    async def delete(self, id: int)->None:
        logger.info(f"Deleting record with ID {id}.")
        stmt = delete(self.model).filter(self.model.id == id) # type: ignore
        await self.session.execute(stmt)
        await self.session.flush()
        logger.info(f"Record with ID {id} successfully deleted.")
