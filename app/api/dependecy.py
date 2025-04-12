from app.repositories.repository import GroupRepository, ScheduleRepository
from app.repositories.repository import RoomRepository
from app.repositories.repository import StudentRepository
from app.repositories.repository import SubjectRepository
from app.repositories.repository import TeacherRepository
from app.services.group_service import GroupService
from app.services.room_service import RoomService
from app.services.schedule_service import ScheduleService
from app.services.student_services import StudentService
from app.services.subject_service import SubjectService
from app.services.teacher_service import TeacherService
from app.db.database import async_session_maker


async def get_async_session():
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_group_service():
    return GroupService(GroupRepository())


async def get_room_service():
    return RoomService(RoomRepository())


async def get_student_service():
    return StudentService(StudentRepository())


async def get_subject_service():
    return SubjectService(SubjectRepository())


async def get_teacher_service():
    return TeacherService(TeacherRepository())


async def get_schedule_service():
    return ScheduleService(ScheduleRepository())
