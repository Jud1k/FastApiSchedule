import json
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictException, NotFoundException
from app.domain.group.repository import GroupRepository
from app.domain.group.schemas import GroupCreate, GroupUpdate
from app.db.models import Group
from app.cache.custom_redis import CustomRedis

logger = logging.getLogger(__name__)


class CacheKeys:
    GROUPS = "groups"


class GroupService:
    def __init__(self, session: AsyncSession, redis: CustomRedis):
        self.group_repo = GroupRepository(session)
        self.redis = redis

    async def get_all(self) -> list[Group | None]:
        cache_key = CacheKeys.GROUPS
        cached_data = await self.redis.get_cached_data(cache_key, self.group_repo.get_all)
        return cached_data

    async def get_by_id(self, group_id: int) -> Group | None:
        group = await self.group_repo.get_one_or_none_by_id(id=group_id)
        return group
    
    async def get_groups_summary(self):
        groups = await self.group_repo.get_groups_summary()
        return groups

    async def create(self, group_in: GroupCreate) -> Group:
        try:
            group = await self.group_repo.create(data=group_in)
            await self.redis.delete_key(CacheKeys.GROUPS)
            return group
        except IntegrityError as e:
            logger.error(f"Error while creating group: {str(e)}")
            raise ConflictException("Group")
        
    async def update(self, group_id: int, group_in: GroupUpdate) -> Group:
        group = await self.group_repo.get_one_or_none_by_id(id=group_id)
        if group is None:
            raise NotFoundException("Group",group_id)
        try:
            group = await self.group_repo.update(data=group, update_data=group_in)
            await self.redis.delete_key(CacheKeys.GROUPS)
            return group
        except IntegrityError as e:
            logger.error(f"Integirity error while updating group: {str(e)}")
            raise ConflictException("Group")
        
    async def delete(self, group_id: int):
        group = await self.group_repo.get_one_or_none_by_id(id=group_id)
        if not group:
            raise NotFoundException("Group",group_id)
        await self.redis.delete_key("groups")
        await self.group_repo.delete(id=group_id)

    async def search_groups(self, query: str) -> list[Group]:
        cache_key = f"group:search:%{query.lower()}"
        cached_data = await self.redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
        groups = await self.group_repo.search(query=query)
        await self.redis.set_value_with_ttl(
            cache_key, 3600, json.dumps([g.to_dict() for g in groups])
        )
        return groups
