from typing import Self
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict,
    model_validator,
    computed_field
)

from app.core.security import get_password_hash


class EmailModel(BaseModel):
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserRegister(EmailModel):
    password: str = Field(
        min_length=5, max_length=50, description="Password 5-50 symbols"
    )
    confirm_password: str = Field(
        min_length=5, max_length=50, description="Repeat password"
    )


class UserToDB(EmailModel):
    password: str = Field(
        min_length=5, max_length=50, description="Password 5-50 symbols"
    )


class UserAuth(EmailModel):
    password: str = Field(min_length=5)


class RoleModel(BaseModel):
    id: int = Field(description="Role id")
    name: str = Field(description="Role name")
    model_config = ConfigDict(from_attributes=True)


class UserInfo(UserAuth):
    id: int
    role: RoleModel = Field(exclude=True)

    @computed_field
    def role_name(self)->str:
        return self.role.name
    
    @computed_field
    def role_id(self)->int:
        return self.role.id