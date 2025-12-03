from datetime import timedelta
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.limiter import limiter
from app.domain.auth.schemas import (
    AuthResponse,
    PasswordChange,
    UserRead,
    UserRegister,
)
from app.core.config import settings
from app.core.deps.auth import (
    CurrentUser,
    get_refresh_token,
)
from app.core.deps.service import AuthServiceDep
from app.domain.auth.utils import (
    verify_password,
)
from app.exceptions import (
    ConflictException,
    IncorrectEmailOrPasswordException,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Auth"])


@router.post("/register/", response_model=UserRead,status_code=status.HTTP_201_CREATED)
@limiter.limit("5/hour")
async def register_user(request:Request,user_in: UserRegister, service: AuthServiceDep):
    user = await service.get_by_email(email=user_in.email)
    if user:
        raise ConflictException("User")
    user = await service.create(user_in=user_in)
    return user


@router.get("/debug/cookies")
async def debug_cookies(request: Request):
    return {"cookies": request.cookies, "headers": dict(request.headers)}


@router.post("/login/", response_model=AuthResponse)
async def login_user(
    response: Response,
    service: AuthServiceDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await service.get_by_email(email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise IncorrectEmailOrPasswordException
    access_token = service.create_access_token(
        user_id=user.id,
        email=user.email,
        role=user.role,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = await service.create_refresh_token(
        user_id=user.id,
        email=user.email,
        role=user.role,
        expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=30 * 24 * 60 * 60,
    )
    user_data = UserRead.model_validate(user)
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_data,
    )


@router.post("/logout/")
async def logout_user(
    response: Response,
    service: AuthServiceDep,
    token: str = Depends(get_refresh_token),
):
    try:
        await service.revoke_refresh_token(token=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    response.delete_cookie("refresh_token")
    return {"message": "Successfully logout"}


@router.patch("/change-password/")
@limiter.limit("5/hour")
async def change_password(
    request: Request,
    request_body:PasswordChange,
    service: AuthServiceDep,
    current_user: CurrentUser,
    refresh_token: str = Depends(get_refresh_token),
):
    await service.revoke_refresh_token(token=refresh_token)
    await service.update_user_password(user_id=current_user.id, new_password=request_body.new_password)
    return {"message": "Password updated successfully"}


@router.get("/users/", response_model=list[UserRead])
async def get_all_users(
    service: AuthServiceDep,
):
    return await service.get_all()


@router.get("/check/", response_model=UserRead)
async def check_auth(user_data: CurrentUser):
    return user_data


@router.post("/refresh/", response_model=AuthResponse)
async def process_refresh_token(
    response: Response,
    service: AuthServiceDep,
    refresh_token: str = Depends(get_refresh_token),
):
    try:
        payload = await service.validate_refresh_token(token=refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    user = await service.get_by_id(user_id=payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    access_token = service.create_access_token(
        user_id=payload["sub"],
        email=user.email,
        role=user.role,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    new_refresh_token = await service.create_refresh_token(
        user_id=payload["sub"],
        email=user.email,
        role=user.role,
        expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
    )
    await service.revoke_refresh_token(token=refresh_token)
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=30 * 24 * 60 * 60,
    )
    user_data = UserRead.model_validate(user)
    return AuthResponse(access_token=access_token, refresh_token=new_refresh_token, user=user_data)
