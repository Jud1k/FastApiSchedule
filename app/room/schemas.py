from datetime import datetime

from pydantic import BaseModel, Field

from app.building.schemas import BuildingRead


class RoomBase(BaseModel):
    name: str
    floor: int
    capacity: int
    status: int = Field(description="0 - Not available, 1 - Available")
    building_id: int


class RoomRead(RoomBase):
    id: int
    building: BuildingRead
    created_at: datetime
    updated_at: datetime


class RoomCreate(RoomBase):
    pass


class RoomUpdate(RoomBase):
    pass
