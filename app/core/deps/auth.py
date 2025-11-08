import logging

from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError

from app.auth.schemas import UserRead
from app.auth.token_service import TokenService
from app.core.deps.service import get_token_service
from app.exceptions import (
    ForbiddenException,
    MissingCoockies,
    NoJwtException,
    TokenExpiredException,
    TokenNoFound,
)
from app.shared.models import User

logger = logging.getLogger(__name__)


def get_access_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise TokenNoFound
    access_token = auth_header.split(" ")[1]
    return access_token


def get_refresh_token(request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise MissingCoockies
    return token


async def get_current_user(
    token: str = Depends(get_access_token),
    token_service: TokenService = Depends(get_token_service),
) -> UserRead:
    try:
        payload = token_service._decode_token(token=token)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise NoJwtException
    return UserRead(email=payload.email, id=int(payload.sub), role=payload.role)


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role_id in [2, 3]:
        return current_user
    raise ForbiddenException
