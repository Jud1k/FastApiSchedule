import logging
import uuid
from datetime import timedelta

from jose import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.repository import UserRepository
from app.domain.auth.schemas import UserBase, UserCreate
from app.domain.auth.utils import create_token, decode_token
from app.domain.auth.utils import get_password_hash
from app.db.models import User
from app.cache.custom_redis import CustomRedis
from app.exceptions import NoJwtException, TokenExpiredException

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, session: AsyncSession, redis: CustomRedis):
        self.user_repo = UserRepository(session)
        self.redis = redis

    async def get_by_email(self, email: str) -> User | None:
        user = await self.user_repo.get_one_or_none(filters=UserBase(email=email))
        return user

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        user = await self.user_repo.get_user_by_id(user_id=user_id)
        return user

    async def get_all(self) -> list[User]:
        users = await self.user_repo.get_all()
        return users

    async def create(self, user_in: UserCreate) -> User:
        hashed_password = get_password_hash(user_in.password)
        user_in.password = hashed_password
        user = await self.user_repo.create(data=user_in)
        return user
    
    async def update_user_password(self, user_id:uuid.UUID, new_password: str) -> None:
        hashed_password = get_password_hash(new_password)
        await self.user_repo.update_user_password(user_id=user_id,new_password=hashed_password)
        
    def create_access_token(
        self, user_id: uuid.UUID, email: str, role: str, expires_delta: timedelta
    ) -> str:
        jti = uuid.uuid4()
        token_data = {
            "sub": str(user_id),
            "email": email,
            "role": role,
            "type": "access",
            "jti": str(jti),
        }
        access_token = create_token(token_data, expires_delta)
        return access_token

    async def create_refresh_token(
        self, user_id: uuid.UUID, email: str, role: str, expires_delta: timedelta
    ) -> str:
        jti = uuid.uuid4()
        token_data = {
            "sub": str(user_id),
            "email": email,
            "role": role,
            "type": "refresh",
            "jti": str(jti),
        }
        refresh_token = create_token(token_data, expires_delta)
        await self.redis.set_value_with_ttl(
            key=f"refresh_token:{jti}", value=str(user_id), ttl=604800
        )
        return refresh_token

    async def revoke_refresh_token(self, token: str):
        try:
            payload = decode_token(token=token)
        except ExpiredSignatureError:
            raise TokenExpiredException
        except JWTError:
            raise NoJwtException
        if payload["type"] != "refresh":
            raise ValueError("Invalid token type")
        await self.redis.delete_key(f"refresh_token:{payload['jti']}")

    async def validate_refresh_token(self, token: str) -> dict:    
        try:
            payload = decode_token(token=token)
        except ExpiredSignatureError:
            raise TokenExpiredException
        except JWTError:
            raise NoJwtException
        if payload["type"] != "refresh":
            raise ValueError("Invalid token type")
        return payload
