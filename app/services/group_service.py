import json
import logging

from app.redis.custom_redis import CustomRedis
from app.api.schemas.group import GroupFromDB, GroupToCreate
from app.exceptions import ConflictError, NotFoundError
from app.repositories.repository import GroupRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


logger = logging.getLogger(__name__)


class CacheKeys:
    GROUPS = "groups"


class GroupService:
    def __init__(self, session: AsyncSession, redis: CustomRedis):
        self.group_repo = GroupRepository(session)
        self.redis = redis

    async def get_all(self) -> list[GroupFromDB]:
        cache_key = CacheKeys.GROUPS
        cached_data = await self.redis.get_cached_data(
            cache_key, self.group_repo.get_all
        )
        return cached_data

    async def get_one_by_id(self, group_id: int) -> GroupFromDB:
        group = await self.group_repo.get_one_or_none_by_id(id=group_id)
        if not group:
            logger.error(f"Group with {group_id} id does not exist")
            raise NotFoundError("An group with this id does not exist")
        return group

    async def create(self, group_in: GroupToCreate) -> GroupFromDB:
        group = await self.group_repo.get_one_or_none(filters=group_in)
        if group:
            logger.error(f"Group with name {group.name} already exist")
            raise ConflictError("An group with this name already exist")
        await self.redis.delete_key("groups")
        data = group_in.model_dump()
        return await self.group_repo.create(data=data)

    async def update(self, group_id: int, group_in: GroupToCreate) -> GroupFromDB:
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
        await self.redis.delete_key("groups")
        return group

    async def delete(self, group_id: int):
        group = await self.group_repo.get_one_or_none_by_id(id=group_id)
        if not group:
            logger.error(f"Group with {group_id} id does not exist")
            raise NotFoundError("An group with this id does not exist")
        await self.redis.delete_key("groups")
        await self.group_repo.delete(id=group_id)

    async def search_groups(self, query: str) -> list[GroupFromDB]:
        cache_key = f"group:search:%{query.lower()}"
        cached_data = await self.redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
        groups = await self.group_repo.search(query=query)
        await self.redis.set_value_with_ttl(
            cache_key, 3600, json.dumps([g.to_dict() for g in groups])
        )
        return groups
