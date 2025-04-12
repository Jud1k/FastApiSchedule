import logging
from typing import Type
from app.api.schemas.group import GroupFromDB, GroupToCreate
from app.repositories.repository import GroupRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException


logger = logging.getLogger(__name__)


class GroupService:
    def __init__(self, group_repo: GroupRepository):
        self.group_repo = group_repo

    async def get_all(self, session: AsyncSession) -> list[GroupFromDB]:
        async with session.begin():
            return await self.group_repo.get_all(session)

    async def get_one_by_id(self, session: AsyncSession, group_id: int) -> GroupFromDB:
        async with session.begin():
            record = await self.group_repo.get_one_or_none_by_id(
                id=group_id, session=session
            )
            if not record:
                raise HTTPException(
                    status_code=404, detail=f"Record with {group_id} id does not exist"
                )
            return record

    async def create(
        self, session: AsyncSession, group_data: GroupToCreate
    ) -> GroupFromDB:
        async with session.begin():
            data = group_data.model_dump()
            try:
                return await self.group_repo.create(data=data, session=session)
            except IntegrityError:
                raise HTTPException(
                    status_code=400,
                    detail="Group with this name alredy exist",
                )

    async def update(
        self, session: AsyncSession, group_id: int | None, group_data: GroupToCreate
    ) -> GroupFromDB:
        async with session.begin():
            group = await self.group_repo.get_one_or_none_by_id(
                id=group_id, session=session
            )
            if not group:
                raise HTTPException(
                    status_code=404, detail=f"Record with {group_id} id does not exist"
                )
            try:
                update_group_data = group_data.model_dump(exclude_unset=True)
                return await self.group_repo.update(
                    obj=group, update_data=update_group_data, session=session
                )
            except IntegrityError as e:
                raise HTTPException(
                    status_code=400, detail="Group with this name alredy exist"
                )

    async def delete(
        self, session: AsyncSession, group_id: int, delete_all: bool = False
    ) -> int:
        async with session.begin():
            try:
                return await self.group_repo.delete(
                    id=group_id, delete_all=delete_all, session=session
                )
            except SQLAlchemyError:
                raise HTTPException(
                    status_code=400, detail="Something went wrong. Try again"
                )

    async def search_groups(self, session: AsyncSession, query: str) -> list[dict]:
        return await self.group_repo.search_groups(session=session, query=query)
