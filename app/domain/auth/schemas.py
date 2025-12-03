import uuid
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)


class UserBase(BaseModel):
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str
    role:str|None=None

class UserRegister(UserCreate):
    pass

class UserRead(UserBase):
    id: uuid.UUID
    role: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class AuthResponse(TokenPair):
    user: UserRead

class PasswordChange(BaseModel):
    new_password:str