from typing import List
from pydantic import BaseModel
from datetime import date

class TeacherBase(BaseModel):
    last_name: str
    position: str
    subject: str

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int

    class Config:
        orm_mode = True

class ExamBase(BaseModel):
    subject: str
    group_number: str
    exam_date: date

class ExamCreate(ExamBase):
    teacher_id: int  # привязка экзамена к учителю

class Exam(ExamBase):
    id: int
    teacher_id: int

    class Config:
        orm_mode = True

# Новая схема для возврата учителя с экзаменами
class TeacherExams(BaseModel):
    teacher: Teacher
    exams: List[Exam]

    class Config:
        orm_mode = True
