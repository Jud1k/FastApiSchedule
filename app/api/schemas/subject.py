from datetime import datetime
from pydantic import BaseModel


class SubjectFromDB(BaseModel):
    id: int
    name:str
    created_at: datetime
    updated_at: datetime


class SubjectToCreate(BaseModel):
    name:str
