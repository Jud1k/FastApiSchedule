from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory,T
from app.shared.models import Building, Group, Room, Subject,Student, Teacher, Lesson

class BaseSqlAlchemyFactory(SQLAlchemyFactory[T]):
    __is_base_factory__=True
    __check_model__=True
    __set_relationships__=True
    __set_foreign_keys__=True
    
class SubjectFactory(BaseSqlAlchemyFactory[Subject]):
    __model__=Subject
    
class RoomFactory(BaseSqlAlchemyFactory[Room]):
    __model__=Room
        
class BuildingFactory(BaseSqlAlchemyFactory[Building]):
    __model__=Building
    
class GroupFactory(BaseSqlAlchemyFactory[Group]):
    __model__=Group
    
class StudentFactory(BaseSqlAlchemyFactory[Student]):
    __model__=Student
    
class LessonFactory(BaseSqlAlchemyFactory[Lesson]):
    __model__=Lesson
    
class TeacherFactory(BaseSqlAlchemyFactory[Teacher]):
    __model__=Teacher
    
    email=BaseSqlAlchemyFactory.__faker__.email