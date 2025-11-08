from datetime import date, datetime

from pydantic import BaseModel, EmailStr


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    phone: str
    course: int
    group_id: int


class StudentRead(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass
