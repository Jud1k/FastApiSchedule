from datetime import datetime
from pydantic import BaseModel


class RoomFromDB(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class RoomToCreate(BaseModel):
    name: str
