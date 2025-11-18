from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.building.schemas import BuildingRead


class RoomBase(BaseModel):
    name: str
    floor: int
    capacity: int
    status: int = Field(description="0 - Not available, 1 - Available")
    building_id: int

    model_config = ConfigDict(from_attributes=True)
    
class RoomRead(RoomBase):
    id: int
    building: BuildingRead
    created_at: datetime
    updated_at: datetime

class RoomReadMinimal(RoomBase):
    id:int
    
class RoomCreate(RoomBase):
    pass


class RoomUpdate(RoomBase):
    pass
