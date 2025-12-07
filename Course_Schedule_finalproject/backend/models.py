# backend/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    courses = relationship("Course", back_populates="instructor")


# backend/models.py
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # NEW: mã môn học (교과목코드) để phân nhóm
    course_code = Column(String, nullable=True)
    department = Column(String, nullable=True) # 학과
    credits = Column(Integer, nullable=False)
    num_weeks = Column(Integer, nullable=False)
    students = Column(Integer, nullable=False)

    # NEW: năm học + lớp (3A, 3B...)
    class_year = Column(Integer, nullable=False)   # 개설학년
    section = Column(String, nullable=True)        # "3A", "3B" ...

    instructor_id = Column(Integer, ForeignKey("instructors.id"), nullable=False)
    instructor = relationship("Instructor", back_populates="courses")

    schedules = relationship("Schedule", back_populates="course")


class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)

    schedules = relationship("Schedule", back_populates="classroom")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    week = Column(Integer, nullable=False)         # luôn = 1 (tuần mẫu)
    day = Column(String, nullable=False)           # Mon..Fri
    start_period = Column(Integer, nullable=False) # 1..8
    num_periods = Column(Integer, nullable=False)  # số tiết liên tục

    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)

    course = relationship("Course", back_populates="schedules")
    classroom = relationship("Classroom", back_populates="schedules")
