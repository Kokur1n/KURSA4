from sqlalchemy.orm import Session
from models import Teacher, Exam
from schemas import TeacherCreate, ExamCreate


# CRUD для Teachers

def get_teachers(db: Session):
    """Получить список всех учителей."""
    return db.query(Teacher).all()


def get_teacher(db: Session, teacher_id: int):
    """Получить учителя по идентификатору."""
    return db.query(Teacher).filter(Teacher.id == teacher_id).first()


def create_teacher(db: Session, teacher: TeacherCreate):
    """Создать нового учителя."""
    db_teacher = Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


def update_teacher(db: Session, teacher_id: int, teacher_data: TeacherCreate):
    """Обновить данные учителя."""
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if db_teacher:
        for key, value in teacher_data.dict().items():
            setattr(db_teacher, key, value)
        db.commit()
        db.refresh(db_teacher)
    return db_teacher


def delete_teacher(db: Session, teacher_id: int):
    """Удалить учителя."""
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if db_teacher:
        db.delete(db_teacher)
        db.commit()
    return db_teacher


# CRUD для Exams

def get_exams(db: Session):
    """Получить список всех экзаменов."""
    return db.query(Exam).all()


def get_exam(db: Session, exam_id: int):
    """Получить экзамен по идентификатору."""
    return db.query(Exam).filter(Exam.id == exam_id).first()


def create_exam(db: Session, exam: ExamCreate):
    """Создать новый экзамен с привязкой к учителю."""
    db_exam = Exam(**exam.dict())
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam


def update_exam(db: Session, exam_id: int, exam_data: ExamCreate):
    """Обновить данные экзамена."""
    db_exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if db_exam:
        for key, value in exam_data.dict().items():
            setattr(db_exam, key, value)
        db.commit()
        db.refresh(db_exam)
    return db_exam


def delete_exam(db: Session, exam_id: int):
    """Удалить экзамен."""
    db_exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if db_exam:
        db.delete(db_exam)
        db.commit()
    return db_exam


def get_teacher_exams(db: Session, teacher_id: int):
    """
    Получить учителя и список экзаменов, привязанных к нему.
    Если учитель не найден, возвращается (None, None).
    """
    teacher = get_teacher(db, teacher_id)
    if teacher is None:
        return None, None
    exams = db.query(Exam).filter(Exam.teacher_id == teacher_id).all()
    return teacher, exams


def search_teachers(db: Session, query: str):
    """Поиск учителей по фамилии."""
    return db.query(Teacher).filter(Teacher.last_name.ilike(f"%{query}%")).all()


def search_exams(db: Session, query: str):
    """Поиск экзаменов по предмету."""
    return db.query(Exam).filter(Exam.subject.ilike(f"%{query}%")).all()
