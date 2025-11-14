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
    role: str|None = None


class UserRegister(UserCreate):
    pass


class UserLogin(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    role: str


class TokenPayload(BaseModel):
    sub: int  # user_id
    email: EmailStr
    role: str
    exp: int
    jti: str | None = None
    type: str | None = None


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class AuthResponse(TokenPair):
    user: UserRead
