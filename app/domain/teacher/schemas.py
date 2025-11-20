from datetime import datetime

from pydantic import BaseModel, EmailStr


class TeacherBase(BaseModel):
    first_name: str
    middle_name:str|None
    last_name:str
    email: EmailStr|None
    phone: str|None
    department: str
    title: str


class TeacherRead(TeacherBase):
    id: int
    created_at: datetime
    updated_at: datetime


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(TeacherBase):
    pass
