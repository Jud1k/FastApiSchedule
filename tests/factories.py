from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory,T
from app.db.models import Building, Group, Room, Subject,Student, Teacher, Lesson, User
from app.domain.auth.utils import get_password_hash

class BaseSqlAlchemyFactory(SQLAlchemyFactory[T]):
    __is_base_factory__=True
    __check_model__=True
    __set_primary_key__=False
    __set_relationships__=True
    __set_foreign_keys__=True

class SubjectFactory(BaseSqlAlchemyFactory[Subject]):
    __model__=Subject
         
class BuildingFactory(BaseSqlAlchemyFactory[Building]):
    __model__=Building
    
class RoomFactory(BaseSqlAlchemyFactory[Room]):
    __model__=Room
    
class GroupFactory(BaseSqlAlchemyFactory[Group]):
    __model__=Group
    
class StudentFactory(BaseSqlAlchemyFactory[Student]):
    __model__=Student
    
class TeacherFactory(BaseSqlAlchemyFactory[Teacher]):
    __model__=Teacher

    email=BaseSqlAlchemyFactory.__faker__.email
    
class LessonFactory(BaseSqlAlchemyFactory[Lesson]):
    __model__=Lesson
    
    teacher = TeacherFactory
    
class UserFactory(BaseSqlAlchemyFactory[User]):
    __model__=User
    
    email= BaseSqlAlchemyFactory.__faker__.email
    password = get_password_hash(BaseSqlAlchemyFactory.__faker__.password(special_chars=False))
    role="user"
    