from datetime import datetime, date
from pydantic import BaseModel,EmailStr

class TeacherFromDB(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    phone: str
    created_at:datetime
    updated_at:datetime

class TeacherToCreate(BaseModel):
    first_name:str
    last_name:str
    date_of_birth: date
    email: EmailStr
    phone: str
