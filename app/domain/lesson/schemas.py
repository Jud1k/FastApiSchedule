from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.group.schemas import GroupRead
from app.domain.room.schemas import RoomReadMinimal
from app.domain.subject.schemas import SubjectRead
from app.domain.teacher.schemas import TeacherRead


class LessonBase(BaseModel):
    time_id: int
    day_of_week: int
    type: str

    model_config = ConfigDict(from_attributes=True)
    
class LessonRead(LessonBase):
    id: int
    subject_id: int
    teacher_id: int
    room_id: int
    group_id: int
    group: GroupRead
    subject: SubjectRead
    teacher: TeacherRead
    room: RoomReadMinimal
    created_at: datetime
    updated_at: datetime

class LessonReadMinimal(LessonBase):
    id:int
    subject_id: int
    teacher_id: int
    room_id: int
    group_id: int
    
class LessonCreate(LessonBase):
    subject_id: int
    teacher_id: int
    room_id: int
    group_id: int


class LessonUpdate(LessonBase):
    subject_id: int
    teacher_id: int
    room_id: int
    group_id: int


class LessonById(BaseModel):
    id: int
    time_id: int
    day_of_week: int
    type: str
    group: GroupRead
    subject: SubjectRead
    teacher: TeacherRead
    room: RoomReadMinimal