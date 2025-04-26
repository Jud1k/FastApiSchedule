import logging
from app.api.schemas.group import GroupFromDB, GroupToCreate
from app.exceptions import ConflictError, NotFoundError
from app.repositories.repository import GroupRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


logger = logging.getLogger(__name__)


class GroupService:
    def __init__(self, session: AsyncSession):
        self.group_repo = GroupRepository(session)

    async def get_all(self) -> list[GroupFromDB]:
        return await self.group_repo.get_all()

    async def get_one_by_id(self, group_id: int) -> GroupFromDB:
        group = await self.group_repo.get_one_or_none_by_id(id=group_id)
        if not group:
            logger.error(f"Group with {group_id} id does not exist")
            raise NotFoundError("An group with this id does not exist")
        return group

    async def create(self, group_in: GroupToCreate) -> GroupFromDB:
        group = await self.group_repo.get_by_name(name=group_in.name)
        if group:
            logger.error(f"Group with name {group.name} already exist")
            raise ConflictError("An group with this name already exist")
        data = group_in.model_dump()
        return await self.group_repo.create(data=data)

    async def update(
        self, group_id: int, group_in: GroupToCreate
    ) -> GroupFromDB:
        group = await self.group_repo.get_one_or_none_by_id(id=group_id)
        if not group:
            logger.error(f"Group with {group_id} id does not exist")
            raise NotFoundError("An group with this id does not exist")
        try:
            update_data = group_in.model_dump(exclude_unset=True)
            group = await self.group_repo.update(data=group, update_data=update_data)
        except IntegrityError as e:
            logger.error({e})
            raise ConflictError("An group with this name alredy exist")
        return group

    async def delete(self, group_id: int):
        group = await self.group_repo.get_one_or_none_by_id(id=group_id)
        if not group:
            logger.error(f"Group with {group_id} id does not exist")
            raise NotFoundError("An group with this id does not exist")
        await self.group_repo.delete(id=group_id)

    async def search_groups_by_name(self, query: str) -> list[GroupFromDB]:
        return await self.group_repo.search_by_name(query=query)
