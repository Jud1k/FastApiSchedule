from typing import Optional
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict,
    computed_field,
)


class UserBase(BaseModel):
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class RoleModel(BaseModel):
    id: int = Field(description="Role id")
    name: str = Field(description="Role name")
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
    password: str
    role_id: int


class UserInfo(UserBase):
    id: int
    role_name: str


class UserWithRole(UserBase):
    id: int
    role: RoleModel = Field(exclude=True)

    @computed_field
    @property
    def role_name(self) -> str:
        return self.role.name


class UserLogin(UserWithRole):
    password: str


class TokenPayload(BaseModel):
    sub: int  # user_id
    email: EmailStr
    role: str
    exp: int
    jti: Optional[str] = None
    type: Optional[str] = None


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class AuthResponse(TokenPair):
    user: UserWithRole
