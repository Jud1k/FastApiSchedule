import logging
from typing import Annotated
import uuid

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError

from app.core.deps.service import AuthServiceDep
from app.domain.auth.schemas import UserRead
from app.domain.auth.utils import decode_token
from app.exceptions import (
    ForbiddenException,
    MissingCoockies,
    NoJwtException,
    NotFoundException,
    TokenExpiredException,
)

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/")


def get_refresh_token(request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        logger.warning("No refresh token")
        raise MissingCoockies
    return token


async def get_current_user(
    service:AuthServiceDep,
    token:str= Depends(oauth2_scheme),
) -> UserRead:
    try:
        payload = decode_token(token=token)
    except ExpiredSignatureError:
        logger.warning("Access token expired.")
        raise TokenExpiredException
    except JWTError:
        logger.warning("Access token not valid.")
        raise NoJwtException
    user = await service.get_by_id(user_id=uuid.UUID(payload["sub"]))
    if not user:
        logger.warning(f"User with ID {payload["sub"]} not found.")
        raise NotFoundException("User", payload["sub"])
    return UserRead.model_validate(user)

CurrentUser = Annotated[UserRead,Depends(get_current_user)]

async def get_current_admin_user(current_user: CurrentUser):
    if current_user.role == "admin":
        return current_user
    raise ForbiddenException

AdminUser = Annotated[UserRead,Depends(get_current_admin_user)]