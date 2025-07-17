from fastapi import Depends
from app.redis.custom_redis import CustomRedis
from app.services.token_service import TokenService
from app.services.group_service import GroupService
from app.services.room_service import RoomService
from app.services.schedule_service import ScheduleService
from app.services.student_services import StudentService
from app.services.subject_service import SubjectService
from app.services.teacher_service import TeacherService
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.redis.manager import get_redis
from app.services.user_service import UserService


async def get_group_service(
    session: AsyncSession = Depends(get_db), redis: CustomRedis = Depends(get_redis)
):
    return GroupService(session=session, redis=redis)


async def get_token_service(redis: CustomRedis = Depends(get_redis)):
    return TokenService(redis=redis)


async def get_room_service(session: AsyncSession = Depends(get_db)):
    return RoomService(session=session)


async def get_student_service(session: AsyncSession = Depends(get_db)):
    return StudentService(session)


async def get_subject_service(session: AsyncSession = Depends(get_db)):
    return SubjectService(session)


async def get_teacher_service(session: AsyncSession = Depends(get_db)):
    return TeacherService(session)


async def get_schedule_service(session: AsyncSession = Depends(get_db)):
    return ScheduleService(session=session)


async def get_user_service(session: AsyncSession = Depends(get_db)):
    return UserService(session=session)
