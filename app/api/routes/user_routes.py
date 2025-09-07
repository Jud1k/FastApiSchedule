import logging
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.api.schemas.user import (
    AuthResponse,
    UserBase,
    UserCreate,
    UserFromDB,
    UserInfo,
    UserWithRole,
)
from app.api.dependencies.service_dep import get_token_service, get_user_service
from app.api.dependencies.auth_dep import (
    get_current_user,
    get_refresh_token,
)
from app.core.security import (
    authenticate_user,
    get_password_hash,
)
from app.db.models import User
from app.services.token_service import TokenService
from app.services.user_service import UserService
from app.exceptions import (
    IncorrectEmailOrPasswordException,
    UserAlreadyExistsException,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/")
async def register_user(
    user_data: UserCreate, service: UserService = Depends(get_user_service)
):
    user = await service.get_one_or_none(filters=UserBase(email=user_data.email))
    if user:
        raise UserAlreadyExistsException
    user_data.password = get_password_hash(user_data.password)
    user_data_dict = user_data.model_dump()
    await service.create(user_in=user_data_dict)
    return {"msg": "You sucessfuly register"}


@router.get("/debug/cookies")
async def debug_cookies(request: Request):
    return {"cookies": request.cookies, "headers": dict(request.headers)}


@router.post("/login/", response_model=AuthResponse)
async def login_user(
    response: Response,
    user_data: UserCreate,
    auth_service: TokenService = Depends(get_token_service),
    user_service: UserService = Depends(get_user_service),
) -> dict:
    user = await user_service.get_user_for_login(
        filters=UserBase(email=user_data.email)
    )
    if not user or not await authenticate_user(user=user, password=user_data.password):
        raise IncorrectEmailOrPasswordException
    user_dto = UserWithRole.model_validate(user)
    tokens = await auth_service.create_tokens(user_id=user.id, email=user.email,role=user.role_name)
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
        user=user_dto,
    )


@router.post("/logout/")
async def logout_user(
    response: Response,
    token: str = Depends(get_refresh_token),
    token_service: TokenService = Depends(get_token_service),
) -> dict:
    try:
        await token_service.revoke_refresh_token(token=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    response.delete_cookie("refresh_token")
    return {"message": "The user has successfully logout"}


@router.get("/all_users/", response_model=list[UserFromDB])
async def get_all_users(
    user_service: UserService = Depends(get_user_service),
) -> list[UserFromDB]:
    return await user_service.get_all()


@router.get("/check/", response_model=UserInfo)
async def check_auth(user_data: User = Depends(get_current_user)):
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
    user = await user_service.get_user_by_id(user_id=payload.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    await token_service.revoke_refresh_token(token=token)
    tokens = await token_service.create_tokens(user_id=payload.sub, email=user.email,role=user.role_name)
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=30 * 24 * 60 * 60,
    )
    return {
        "access_token": tokens.access_token,
        "refresh_token": tokens.refresh_token,
        "user": user,
    }
