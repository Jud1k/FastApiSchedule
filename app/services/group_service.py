import logging
from app.api.schemas.group import GroupFromDB, GroupToCreate
from app.repositories.repository import GroupRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException


logger = logging.getLogger(__name__)


class GroupService:
    def __init__(self, session: AsyncSession):
        self.repo = GroupRepository(session)

    async def get_all(self) -> list[GroupFromDB]:
        return await self.repo.get_all()

    async def get_one_by_id(self, group_id: int) -> GroupFromDB:
        record = await self.repo.get_one_or_none_by_id(group_id)
        if not record:
            raise HTTPException(
                status_code=404, detail=f"Record with {group_id} id does not exist"
            )
        return record

    async def create(self, group_data: GroupToCreate) -> GroupFromDB:
        data = group_data.model_dump()
        try:
            return await self.repo.create(data)
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Group with this name alredy exist",
            )

    async def update(
        self, group_id: int | None, group_data: GroupToCreate
    ) -> GroupFromDB:
        group = await self.repo.get_one_or_none_by_id(group_id)
        if not group:
            raise HTTPException(
                status_code=404, detail=f"Record with {group_id} id does not exist"
            )
        try:
            update_group_data = group_data.model_dump(exclude_unset=True)
            return await self.repo.update(group, update_group_data)
        except IntegrityError as e:
            raise HTTPException(
                status_code=400, detail="Group with this name alredy exist"
            )

    async def delete(self, group_id: int, delete_all: bool = False) -> int:
        try:
            return await self.repo.delete(group_id, delete_all)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=400, detail="Something went wrong. Try again"
            )
