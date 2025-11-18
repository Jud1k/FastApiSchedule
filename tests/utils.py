from jose import jwt

from app.core.config import settings

def generate_invalid_token():
    data = {"sub": "sub"}
    token = jwt.encode(data, "secret_key")
    return token


def generate_expired_token():
    data = {"sub": "sub", "exp": 0}
    token = jwt.encode(data,settings.SECRET_KEY,settings.ALGORITHM)
    return token