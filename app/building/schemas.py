from datetime import datetime

from pydantic import BaseModel


class BuildingBase(BaseModel):
    name: str
    address: str


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BuildingBase):
    pass


class BuildingRead(BuildingBase):
    id: int
    created_at: datetime
    updated_at: datetime
