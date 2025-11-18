from datetime import datetime

from pydantic import BaseModel


class SubjectBase(BaseModel):
    name: str
    semester: int
    total_hours: int
    is_optional: bool


class SubjectRead(SubjectBase):
    id: int
    created_at: datetime
    updated_at: datetime


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(SubjectBase):
    pass
