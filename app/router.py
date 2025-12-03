from fastapi import APIRouter

from app.domain.auth.routes import router as user_router
from app.domain.building.routes import router as building_router
from app.domain.group.routes import router as group_router
from app.domain.lesson.routes import router as schedule_router
from app.domain.room.routes import router as room_router
from app.domain.student.routes import router as student_router
from app.domain.subject.routes import router as subject_router
from app.domain.teacher.routes import router as teacher_router
from app.core.utils import router as utils_router


api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(building_router)
api_router.include_router(group_router)
api_router.include_router(schedule_router)
api_router.include_router(room_router)
api_router.include_router(student_router)
api_router.include_router(subject_router)
api_router.include_router(teacher_router)
api_router.include_router(utils_router)

