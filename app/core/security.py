from passlib.context import CryptContext
from fastapi.responses import Response


async def authenticate_user(user, password):
    if not user or not verify_password(
        plain_password=password, hashed_password=user.password
    ):
        return None
    return user


def set_tokens_to_cookie(response: Response, tokens: dict) -> None:
    response.set_cookie(
        key="user_access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=True,
        samesite="lax",
    )

    response.set_cookie(
        key="user_refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="lax",
    )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
