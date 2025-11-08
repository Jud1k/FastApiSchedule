from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.token_service import TokenService
from app.auth.user_service import UserService
from app.building.service import BuildingService
from app.core.database import get_db
from app.group.service import GroupService
from app.lesson.service import LessonService
from app.room.service import RoomService
from app.shared.redis.custom_redis import CustomRedis
from app.shared.redis.manager import get_redis
from app.student.service import StudentService
from app.subject.service import SubjectService
from app.teacher.service import TeacherService


async def get_group_service(
    session: AsyncSession = Depends(get_db), redis: CustomRedis = Depends(get_redis)
):
    return GroupService(session=session, redis=redis)


GroupServiceDep = Annotated[GroupService, Depends(get_group_service)]


async def get_token_service(redis: CustomRedis = Depends(get_redis)):
    return TokenService(redis=redis)


TokenServiceDep = Annotated[TokenService, Depends(get_token_service)]


async def get_room_service(session: AsyncSession = Depends(get_db)):
    return RoomService(session=session)


RoomServiceDep = Annotated[RoomService, Depends(get_room_service)]


async def get_student_service(session: AsyncSession = Depends(get_db)):
    return StudentService(session)


StudentServiceDep = Annotated[StudentService, Depends(get_student_service)]


async def get_subject_service(session: AsyncSession = Depends(get_db)):
    return SubjectService(session)


SubjectServiceDep = Annotated[SubjectService, get_subject_service]


async def get_teacher_service(session: AsyncSession = Depends(get_db)):
    return TeacherService(session)


TeacherServiceDep = Annotated[TeacherService, Depends(get_teacher_service)]


async def get_lesson_service(session: AsyncSession = Depends(get_db)):
    return LessonService(session=session)


LessonServiceDep = Annotated[LessonService, get_lesson_service]


async def get_user_service(session: AsyncSession = Depends(get_db)):
    return UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_building_service(session: AsyncSession = Depends(get_db)):
    return BuildingService(session=session)
