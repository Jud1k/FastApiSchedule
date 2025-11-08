from datetime import datetime

from pydantic import BaseModel, EmailStr


class TeacherBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
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
