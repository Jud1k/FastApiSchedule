from app.repositories.base_repository import BaseRepository
from app.db.models import Student, Subject, Room, Teacher, Group


class StudentRepository(BaseRepository):
    model = Student


class SubjectRepository(BaseRepository):
    model = Subject


class RoomRepository(BaseRepository):
    model = Room


class TeacherRepository(BaseRepository):
    model = Teacher


class GroupRepository(BaseRepository):
    model = Group
