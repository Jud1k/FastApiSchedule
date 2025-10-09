from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date, text
from app.db.database import Base, uniq_str, int_pk


class Student(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[Date] = mapped_column(Date)
    email: Mapped[uniq_str]
    phone: Mapped[str]
    course: Mapped[int]
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=True)

    group: Mapped["Group"] = relationship("Group", back_populates="students")


class Subject(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]
    lessons: Mapped[list["ScheduleLesson"]] = relationship(
        "ScheduleLesson", back_populates="subject", cascade="all,delete-orphan"
    )


class Group(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]

    students: Mapped[list["Student"]] = relationship(
        back_populates="group", cascade="all,delete-orphan"
    )
    lessons: Mapped[list["ScheduleLesson"]] = relationship(
        "ScheduleLesson", back_populates="group", cascade="all,delete-orphan"
    )


class Teacher(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]
    date_of_birth: Mapped[Date] = mapped_column(Date)
    email: Mapped[uniq_str]
    phone: Mapped[uniq_str]

    lessons: Mapped[list["ScheduleLesson"]] = relationship(
        "ScheduleLesson", back_populates="teacher", cascade="all,delete-orphan"
    )


class Room(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]
    lessons: Mapped[list["ScheduleLesson"]] = relationship(
        "ScheduleLesson", back_populates="room", cascade="all,delete-orphan"
    )


class ScheduleLesson(Base):
    id: Mapped[int_pk]
    time_id: Mapped[int]
    day_week: Mapped[int]
    type_lesson: Mapped[str]

    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    subject: Mapped["Subject"] = relationship("Subject", back_populates="lessons")

    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="lessons")

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    room: Mapped["Room"] = relationship("Room", back_populates="lessons")

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship("Group", back_populates="lessons")


class User(Base):
    id: Mapped[int_pk]
    email: Mapped[uniq_str]
    password: Mapped[str]

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), default=1, server_default=text("1")
    )
    role: Mapped["Role"] = relationship("Role", back_populates="users", lazy="joined")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class Role(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]

    users: Mapped[list["User"]] = relationship("User", back_populates="role")
