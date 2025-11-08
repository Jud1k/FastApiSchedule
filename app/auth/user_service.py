import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repository import UserRepository
from app.auth.schemas import UserBase, UserCreate
from app.core.security import get_password_hash
from app.shared.models import User

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)

    async def get_by_email(self, email: str) -> User | None:
        user = await self.user_repo.get_one_or_none(filters=UserBase(email=email))
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        user = await self.user_repo.get_one_or_none_by_id(id=user_id)
        return user

    async def get_all(self) -> list[User]:
        users = await self.user_repo.get_all()
        return users

    async def create(self, user_in: UserCreate) -> User:
        user_in.password = get_password_hash(user_in.password)
        user = await self.user_repo.create(data=user_in.model_dump())
        return user
