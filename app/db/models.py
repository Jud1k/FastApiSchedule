import uuid
from sqlalchemy import Boolean, Date, ForeignKey, UniqueConstraint,Text, String,Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base, int_pk, uniq_str


class Student(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str] = mapped_column(String(100),nullable=False)
    middle_name:Mapped[str] = mapped_column(String(100),nullable=False)
    last_name: Mapped[str] = mapped_column(String(100),nullable=True)
    date_of_birth: Mapped[Date] = mapped_column(Date,nullable=False)
    email: Mapped[str] = mapped_column(String(100),unique=True,nullable=True)
    phone: Mapped[str] = mapped_column(String(18),unique=True,nullable=True)
    course: Mapped[int] = mapped_column(Integer,nullable=False)

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))
    group: Mapped["Group"] = relationship("Group", back_populates="students")


class Subject(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]
    semester: Mapped[int] = mapped_column(Integer,nullable=False)
    total_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    is_optional: Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson", back_populates="subject", cascade="all, delete-orphan"
    )


class Group(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]
    course: Mapped[int] = mapped_column(Integer,nullable=False)
    institute: Mapped[str] = mapped_column(String(100),nullable=False)
    
    students: Mapped[list["Student"]] = relationship(
        "Student",
        back_populates="group",
    )
    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson", back_populates="group", cascade="all, delete-orphan"
    )


class Teacher(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str] = mapped_column(String(100),nullable=False)
    middle_name:Mapped[str] = mapped_column(String(100),nullable=True)
    last_name: Mapped[str] = mapped_column(String(100),nullable=False)
    email: Mapped[str] = mapped_column(String(100),unique=True,nullable=True)
    phone: Mapped[str] = mapped_column(String(18),unique=True,nullable=True)
    department: Mapped[str] = mapped_column(String(50),nullable=False)
    title: Mapped[str] = mapped_column(String(50),nullable=False)
    
    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson", back_populates="teacher", cascade="all, delete-orphan"
    )


class Room(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]
    floor: Mapped[int] = mapped_column(Integer,nullable=False)
    capacity: Mapped[int] = mapped_column(Integer,nullable=False)
    status: Mapped[bool] = mapped_column(Boolean,nullable=False)

    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id", ondelete="CASCADE"))
    building: Mapped["Building"] = relationship("Building", back_populates="rooms")

    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson", back_populates="room", cascade="all, delete-orphan"
    )


class Building(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]
    address: Mapped[uniq_str]

    rooms: Mapped[list["Room"]] = relationship(
        "Room", back_populates="building", cascade="all, delete-orphan"
    )


class Lesson(Base):
    id: Mapped[int_pk]
    time_id: Mapped[int] = mapped_column(Integer,nullable=False)
    day_of_week: Mapped[int] = mapped_column(Integer,nullable=False)
    type: Mapped[str] = mapped_column(String(20),nullable=False)

    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"))
    subject: Mapped["Subject"] = relationship("Subject", back_populates="lessons")

    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"))
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="lessons")

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    room: Mapped["Room"] = relationship("Room", back_populates="lessons")

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))
    group: Mapped["Group"] = relationship("Group", back_populates="lessons")

    __table_args__=(UniqueConstraint("time_id","day_of_week","type","subject_id","teacher_id","room_id","group_id",name="unique_all_fields"),)


class User(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default = uuid.uuid4)
    email: Mapped[uniq_str]
    password: Mapped[str] = mapped_column(Text,nullable=False)
    role: Mapped[str] = mapped_column(Text,server_default="user", default="user")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
