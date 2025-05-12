import logging
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.api.schemas.user import EmailModel, UserInfo, UserAuth
from app.api.dependencies.service_dep import get_auth_service, get_user_service
from app.api.dependencies.auth_dep import get_current_user, get_refresh_token
from app.api.schemas.user import UserRegister
from app.core.security import authenticate_user, get_password_hash, set_tokens_to_cookie
from app.db.models import User
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.exceptions import (
    IncorrectEmailOrPasswordException,
    PasswordsDoNotMatch,
    UserAlreadyExistsException,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register/")
async def register_user(
    user_data: UserRegister, service: UserService = Depends(get_user_service)
) -> dict:
    if user_data.password != user_data.confirm_password:
        raise PasswordsDoNotMatch
    user = await service.get_one_or_none(filters=EmailModel(email=user_data.email))
    if user:
        raise UserAlreadyExistsException
    user_data.password = get_password_hash(user_data.password)
    user_data_dict = user_data.model_dump()
    user_data_dict.pop("confirm_password", None)
    await service.create(user_in=user_data_dict)
    return {"message": "You are successfully registered"}


@router.get("/debug/cookies")
async def debug_cookies(request: Request):
    return {"cookies": request.cookies, "headers": dict(request.headers)}


@router.post("/login/")
async def login_user(
    response: Response,
    user_data: UserAuth,
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
) -> dict:
    user = await user_service.get_one_or_none(filters=EmailModel(email=user_data.email))
    if not user or not await authenticate_user(user=user, password=user_data.password):
        raise IncorrectEmailOrPasswordException
    tokens = await auth_service.create_tokens(user_id=user.id)
    set_tokens_to_cookie(response=response,tokens=tokens)
    return {"ok": "True", "message": "Authorization successful"}


@router.post("/logout/")
async def logout_user(
    response: Response,
    token: str = Depends(get_refresh_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    await auth_service.revoke_refresh_token(token=token)
    response.delete_cookie("user_access_token")
    response.delete_cookie("user_refresh_token")
    return {"message": "The user has successfully logout"}


@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)) -> UserInfo:
    return UserInfo.model_validate(user_data)


@router.get("/all_users/")
async def get_all_users(
    user_service: UserService = Depends(get_user_service),
) -> list[UserInfo]:
    return await user_service.get_all()


@router.post("/refresh/")
async def process_refresh_token(
    response: Response,
    token: str = Depends(get_refresh_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    try:
        payload = await auth_service.validate_refresh_token(token=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    await auth_service.revoke_refresh_token(token=token)
    tokens = await auth_service.create_tokens(user_id=int(payload["sub"]))
    set_tokens_to_cookie(response=response,tokens=tokens)
    return {"message": "Tokens refreshed"}
