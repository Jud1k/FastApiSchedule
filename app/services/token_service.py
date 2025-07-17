from datetime import datetime, timezone, timedelta
from uuid import uuid4
from jose import jwt

from app.api.schemas.user import TokenPair, TokenPayload
from app.core.config import settings
from app.redis.custom_redis import CustomRedis


class TokenService:
    def __init__(self, redis: CustomRedis):
        self.redis = redis

    async def create_tokens(self, user_id: int, email: str) -> TokenPair:
        jti = uuid4().hex

        access_token = self._create_token(
            data={"sub": str(user_id), "email": email, "type": "access"},
            expires_delta=timedelta(minutes=15),
        )

        refresh_token = self._create_token(
            data={"sub": str(user_id), "email": email, "type": "refresh", "jti": jti},
            expires_delta=timedelta(days=7),
        )

        await self.redis.set_value_with_ttl(
            key=f"refresh_token:{jti}",
            ttl=int(timedelta(days=7).total_seconds()),
            value=str(user_id),
        )

        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    def _create_token(self, data: dict, expires_delta: timedelta) -> str:
        now = datetime.now(timezone.utc)
        expires = now + expires_delta
        data.update({"exp": int(expires.timestamp())})
        return jwt.encode(data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    async def revoke_refresh_token(self, token: str) -> None:
        payload = self._decode_token(token)
        if payload.type != "refresh":
            raise ValueError("Invalid token type")
        jti = payload.jti
        if not jti:
            raise ValueError("Invalid token")
        await self.redis.delete_key(f"refresh_token:{jti}")

    def _decode_token(self, token: str) -> TokenPayload:
        payload = jwt.decode(
            token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        return TokenPayload(**payload)

    async def validate_refresh_token(self, token: str) -> TokenPayload:
        payload = self._decode_token(token)
        if payload.type != "refresh":
            raise ValueError("Invalid token type")

        jti = payload.jti
        if not jti or not await self.redis.exists(f"refresh_token:{jti}"):
            raise ValueError("Token revoked or invalid")

        return payload
