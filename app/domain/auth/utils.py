from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def decode_token(token: str) -> dict:
    payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    return payload


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_reset_token(token: str) -> str|None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("email")
    except JWTError:
        return None