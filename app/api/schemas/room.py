from datetime import datetime
from pydantic import BaseModel


class RoomFromDB(BaseModel):
    id: int
    name: str

class RoomToCreate(BaseModel):
    name: str
