import logging

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.auth.schemas import (
    AuthResponse,
    UserLogin,
    UserRead,
    UserRegister,
)
from app.auth.token_service import TokenService
from app.auth.user_service import UserService
from app.core.deps.auth import (
    get_current_user,
    get_refresh_token,
)
from app.core.deps.service import get_token_service, get_user_service
from app.core.security import (
    verify_password,
)
from app.exceptions import (
    IncorrectEmailOrPasswordException,
    UserAlreadyExistsException,
)
from app.shared.models import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/", response_model=UserRead)
async def register_user(user_in: UserRegister, service: UserService = Depends(get_user_service))->User:
    user = await service.get_by_email(email=user_in.email)
    if user:
        raise UserAlreadyExistsException
    user = await service.create(user_in=user_in)
    return user


@router.get("/debug/cookies")
async def debug_cookies(request: Request):
    return {"cookies": request.cookies, "headers": dict(request.headers)}


@router.post("/login/", response_model=AuthResponse)
async def login_user(
    response: Response,
    user_in: UserLogin,
    auth_service: TokenService = Depends(get_token_service),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_by_email(email=user_in.email)
    if not user or verify_password(user_in.password, user.password) is False:
        raise IncorrectEmailOrPasswordException
    tokens = await auth_service.create_tokens(user_id=user.id, email=user.email, role=user.role)
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=30 * 24 * 60 * 60,
    )
    return AuthResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        user=user,
    )


@router.post("/logout/")
async def logout_user(
    response: Response,
    token: str = Depends(get_refresh_token),
    token_service: TokenService = Depends(get_token_service),
):
    try:
        await token_service.revoke_refresh_token(token=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    response.delete_cookie("refresh_token")
    return {"message": "The user has successfully logout"}


@router.get("/all_users/", response_model=list[UserRead])
async def get_all_users(
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_all()


@router.get("/check/", response_model=UserRead)
async def check_auth(user_data: User = Depends(get_current_user))->User:
    return user_data


@router.get("/refresh/", response_model=AuthResponse)
async def process_refresh_token(
    response: Response,
    token: str = Depends(get_refresh_token),
    token_service: TokenService = Depends(get_token_service),
    user_service: UserService = Depends(get_user_service),
) -> AuthResponse:
    try:
        payload = await token_service.validate_refresh_token(token=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    user = await user_service.get_by_id(user_id=payload.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await token_service.revoke_refresh_token(token=token)
    tokens = await token_service.create_tokens(
        user_id=payload.sub, email=user.email, role=user.role
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=30 * 24 * 60 * 60,
    )
    return AuthResponse(access_token=tokens.access_token,refresh_token=tokens.refresh_token,user=user)
