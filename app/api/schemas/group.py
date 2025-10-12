from datetime import datetime
from pydantic import BaseModel


class GroupFromDB(BaseModel):
    id: int
    name: str
    course:int
    institute:str
    created_at: datetime
    updated_at: datetime


class GroupToCreate(BaseModel):
    name: str
    course:int
    institute:str

class GroupSummary(BaseModel):
    id:int
    name: str
    course:int
    institute:str
    count_students:int
