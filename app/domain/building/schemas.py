from datetime import datetime

from pydantic import BaseModel,ConfigDict


class BuildingBase(BaseModel):
    name: str
    address: str

    model_config = ConfigDict(from_attributes=True)
    
class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BuildingBase):
    pass


class BuildingRead(BuildingBase):
    id: int
    created_at: datetime
    updated_at: datetime
