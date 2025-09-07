import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserFromDB, UserLogin, UserToDB, UserWithRole
from app.repositories.repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)

    async def get_one_or_none(self, filters) -> UserFromDB:
        user = await self.user_repo.get_one_or_none(filters=filters)
        return user

    async def get_user_for_login(self, filters) -> UserLogin | None:
        user = await self.user_repo.get_one_or_none(filters=filters)
        if not user:
            return None
        return UserLogin.model_validate(user)

    async def get_user_by_id(self, user_id: int) -> UserWithRole | None:
        user = await self.user_repo.get_one_or_none_by_id(id=user_id)
        if not user:
            return None
        return UserWithRole.model_validate(user)

    async def get_all(self) -> list[UserFromDB]:
        return await self.user_repo.get_all()

    async def create(self, user_in: UserToDB) -> UserFromDB:
        return await self.user_repo.create(data=user_in)
