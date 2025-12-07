# backend/schemas.py
from pydantic import BaseModel
from typing import Optional, List


class InstructorRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ClassroomRead(BaseModel):
    id: int
    name: str
    capacity: int

    class Config:
        orm_mode = True


class CourseRead(BaseModel):
    id: int
    name: str
    course_code: Optional[str]
    department: Optional[str]      # NEW
    credits: int
    num_weeks: int
    students: int
    class_year: int
    section: Optional[str]
    instructor: InstructorRead

    class Config:
        orm_mode = True



class ScheduleRead(BaseModel):
    id: int
    week: int
    day: str
    start_period: int
    num_periods: int
    course: CourseRead         # section nằm trong course
    classroom: ClassroomRead

    class Config:
        orm_mode = True
