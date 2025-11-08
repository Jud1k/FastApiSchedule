from datetime import datetime

from pydantic import BaseModel

from app.group.schemas import GroupRead
from app.room.schemas import RoomRead
from app.subject.schemas import SubjectRead
from app.teacher.schemas import TeacherRead


class LessonBase(BaseModel):
    time_id: int
    day_week: int
    type_lesson: str
    subject_id: int
    teacher_id: int
    room_id: int
    group_id: int


class LessonRead(LessonBase):
    id: int
    group: GroupRead
    subject: SubjectRead
    teacher: TeacherRead
    room: RoomRead
    created_at: datetime
    updated_at: datetime


class LessonCreate(LessonBase):
    pass


class LessonUpdate(LessonBase):
    pass


class LessonByGroupId(LessonBase):
    id: int
    subject: str
    teacher: str
    room: str
