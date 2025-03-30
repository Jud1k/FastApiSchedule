from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey,Date
from app.db.database import Base, uniq_str, str_null_true, int_pk



class Student(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str] = mapped_column(default="1")
    last_name: Mapped[str] = mapped_column(default="1")
    date_of_birth: Mapped[Date] = mapped_column(Date,default="1")
    email: Mapped[uniq_str] = mapped_column(default="1")
    phone: Mapped[uniq_str] = mapped_column(default="1")
    course: Mapped[int] = mapped_column(default="1")
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=True)

    group: Mapped["Group"] = relationship("Group", back_populates="students")


class Subject(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]


class Group(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]
    students: Mapped[list["Student"]] = relationship(back_populates="group")


class Teacher(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[Date]=mapped_column(Date)
    email: Mapped[uniq_str]
    phone: Mapped[uniq_str]


class Room(Base):
    id: Mapped[int_pk]
    name: Mapped[uniq_str]
