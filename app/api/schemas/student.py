from datetime import datetime, date
from pydantic import BaseModel, EmailStr


class StudentFromDB(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    phone: str
    course: int
    group_id: int | None
    created_at: datetime
    updated_at: datetime

class StudentToCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    phone: str
    course: int


class StudentToUpdate(BaseModel):
    first_name: str|None
    last_name: str|None
    date_of_birth: date|None
    email: EmailStr|str|None
    phone: str|None
    course: int|None
