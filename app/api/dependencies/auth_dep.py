import logging
from jose import JWTError, ExpiredSignatureError
from fastapi import Request, Depends

from app.api.schemas.user import UserPublic
from app.api.dependencies.service_dep import get_token_service
from app.db.models import User
from app.services.token_service import TokenService
from app.exceptions import (
    ForbiddenException,
    MissingCoockies,
    NoJwtException,
    TokenExpiredException,
    TokenNoFound,
)

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
) -> UserPublic:
    try:
        payload = token_service._decode_token(token=token)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise NoJwtException
    # expire: str = payload.get("exp")
    # expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    # if (not expire) or (expire_time < datetime.now(timezone.utc)):
    #     raise TokenExpiredException
    return UserPublic(email=payload.email,id=payload.sub)


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role_id in [2, 3]:
        return current_user
    raise ForbiddenException
