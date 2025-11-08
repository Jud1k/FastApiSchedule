from sqlalchemy import Date, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, int_pk, uniq_str


class Student(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[Date] = mapped_column(Date)
    email: Mapped[uniq_str]
    phone: Mapped[str]
    course: Mapped[int]

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))
    group: Mapped["Group"] = relationship("Group", back_populates="students")


class Subject(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]
    semester: Mapped[int]
    total_hours: Mapped[int]
    is_optional: Mapped[bool]
    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson", back_populates="subject", cascade="all, delete-orphan"
    )


class Group(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]
    course: Mapped[int]
    institute: Mapped[str]
    students: Mapped[list["Student"]] = relationship(
        "Student",
        back_populates="group",
    )
    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson", back_populates="group", cascade="all, delete-orphan"
    )


class Teacher(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    email: Mapped[uniq_str]
    phone: Mapped[uniq_str]
    department: Mapped[str]
    title: Mapped[str]
    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson", back_populates="teacher", cascade="all, delete-orphan"
    )


class Room(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]
    floor: Mapped[int]
    capacity: Mapped[int]
    status: Mapped[int] = mapped_column(default=1, server_default=text("1"))

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
    time_id: Mapped[int]
    day_week: Mapped[int]
    type_lesson: Mapped[str]

    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"))
    subject: Mapped["Subject"] = relationship("Subject", back_populates="lessons")

    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"))
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="lessons")

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    room: Mapped["Room"] = relationship("Room", back_populates="lessons")

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))
    group: Mapped["Group"] = relationship("Group", back_populates="lessons")


class User(Base):
    id: Mapped[int_pk]
    email: Mapped[uniq_str]
    password: Mapped[str]
    role: Mapped[str] = mapped_column(server_default="user", default="user")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
