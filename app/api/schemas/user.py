from typing import Optional
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict,
)


class UserBase(BaseModel):
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(
        min_length=5, max_length=50, description="Password 5-50 symbols"
    )


class UserToDB(UserBase):
    id: int
    hashed_password: str


class UserFromDB(UserBase):
    id: int
    hashed_password: str
    role_id: int


class UserPublic(UserBase):
    id: int


class TokenPayload(BaseModel):
    sub: int  # user_id
    email: EmailStr
    exp: int
    jti: Optional[str] = None  # Для refresh-токенов
    type: Optional[str] = None  # "access" или "refresh"


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class AuthResponse(TokenPair):
    user: UserPublic


class RoleModel(BaseModel):
    id: int = Field(description="Role id")
    name: str = Field(description="Role name")
    model_config = ConfigDict(from_attributes=True)
