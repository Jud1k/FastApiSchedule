from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.service import AuthService
from app.domain.building.service import BuildingService
from app.db.database import get_db
from app.domain.group.service import GroupService
from app.domain.lesson.service import LessonService
from app.domain.room.service import RoomService
from app.cache.custom_redis import CustomRedis
from app.cache.manager import get_redis
from app.domain.student.service import StudentService
from app.domain.subject.service import SubjectService
from app.domain.teacher.service import TeacherService


async def get_group_service(
    session: AsyncSession = Depends(get_db), redis: CustomRedis = Depends(get_redis)
):
    return GroupService(session=session, redis=redis)


GroupServiceDep = Annotated[GroupService, Depends(get_group_service)]


async def get_room_service(session: AsyncSession = Depends(get_db)):
    return RoomService(session=session)


RoomServiceDep = Annotated[RoomService, Depends(get_room_service)]


async def get_student_service(session: AsyncSession = Depends(get_db)):
    return StudentService(session)


StudentServiceDep = Annotated[StudentService, Depends(get_student_service)]


async def get_subject_service(session: AsyncSession = Depends(get_db)):
    return SubjectService(session)


SubjectServiceDep = Annotated[SubjectService, Depends(get_subject_service)]


async def get_teacher_service(session: AsyncSession = Depends(get_db)):
    return TeacherService(session)


TeacherServiceDep = Annotated[TeacherService, Depends(get_teacher_service)]


async def get_lesson_service(session: AsyncSession = Depends(get_db)):
    return LessonService(session=session)


LessonServiceDep = Annotated[LessonService, Depends(get_lesson_service)]


async def get_auth_service(session: AsyncSession = Depends(get_db),redis: CustomRedis = Depends(get_redis)):
    return AuthService(session=session,redis=redis)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_building_service(session: AsyncSession = Depends(get_db)):
    return BuildingService(session=session)


BuildingServiceDep = Annotated[BuildingService,Depends(get_building_service)]