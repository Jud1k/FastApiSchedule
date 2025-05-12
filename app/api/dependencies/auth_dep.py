import logging
from datetime import datetime, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Request, Depends

from app.core.config import settings
from app.api.dependencies.service_dep import get_user_service
from app.db.models import User
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.exceptions import (
    ForbiddenException,
    NoJwtException,
    NoUserIdException,
    TokenExpiredException,
    TokenNoFound,
    UserNotFoundException,
)

logger = logging.getLogger(__name__)


def get_access_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise TokenNoFound
    return token


def get_refresh_token(request: Request):
    token = request.cookies.get("user_refresh_token")
    if not token:
        raise TokenNoFound
    return token


async def get_current_user(
    token: str = Depends(get_access_token),
    service: UserService = Depends(get_user_service),
) -> User:
    try:
        payload = jwt.decode(
            token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise NoJwtException
    expire: str = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise NoUserIdException
    user = await service.get_one_or_none_by_id(user_id=int(user_id))
    if not user:
        raise UserNotFoundException
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role_id in [2, 3]:
        return current_user
    raise ForbiddenException
