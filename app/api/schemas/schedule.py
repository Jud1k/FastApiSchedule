from datetime import datetime
from pydantic import BaseModel


class ScheduleToCreate(BaseModel):
    time_id: int
    day_week: int
    type_lesson: str
    subject_id: int
    teacher_id: int
    room_id: int
    group_id: int


class ScheduleFromDB(BaseModel):
    id: int
    time_id: int
    day_week: int
    type_lesson: str
    subject_id: int
    teacher_id: int
    room_id: int
    group_id: int
    created_at: datetime
    updated_at: datetime


class ScheduleWithNames(BaseModel):
    id: int
    time_id: int
    day_week: int
    type_lesson: str
    group: str
    subject: str
    teacher: str
    room: str
