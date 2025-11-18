from datetime import datetime

from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str
    course: int
    institute: str


class GroupRead(GroupBase):
    id: int
    created_at: datetime
    updated_at: datetime


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class GroupSummary(GroupBase):
    id: int
    count_students: int
