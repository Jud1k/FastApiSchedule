from passlib.context import CryptContext
from fastapi.responses import Response
from jose import jwt

from app.core.config import settings


async def authenticate_user(user, password):
    if not user or not verify_password(
        plain_password=password, hashed_password=user.password
    ):
        return None
    return user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def decode_token(token: str):
    return jwt.decode(
        token=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
