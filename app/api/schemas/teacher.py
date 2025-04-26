from datetime import datetime, date
from pydantic import BaseModel,EmailStr

class TeacherFromDB(BaseModel):
    id: int
    name:str
    date_of_birth: date
    email: EmailStr
    phone: str
    created_at:datetime
    updated_at:datetime

class TeacherToCreate(BaseModel):
    name:str
    date_of_birth: date
    email: EmailStr
    phone: str
