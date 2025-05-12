import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserToDB
from app.exceptions import ConflictError
from app.repositories.repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)

    async def get_one_or_none_by_id(self, user_id: int):
        user = await self.user_repo.get_one_or_none_by_id(id=user_id)
        return user

    async def get_one_or_none(self, filters):
        user = await self.user_repo.get_one_or_none(filters=filters)
        return user

    async def get_all(self):
        users = await self.user_repo.get_all()
        return users

    async def create(self, user_in: UserToDB):
        return await self.user_repo.create(data=user_in)
