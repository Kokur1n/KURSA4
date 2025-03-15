from sqlalchemy import Column, Integer, String, Date, ForeignKey  # Импорт типов колонок для таблиц
from sqlalchemy.orm import relationship, validates  # Импорт для создания связей и валидации данных
from database import Base  # Импорт базового класса для моделей SQLAlchemy
import re  # Импорт модуля для работы с регулярными выражениями

# Определение модели Teacher (Учитель)
class Teacher(Base):
    # Указываем имя таблицы в базе данных
    __tablename__ = "teachers"

    # Колонка для уникального идентификатора учителя (первичный ключ)
    id = Column(Integer, primary_key=True, index=True)
    # Колонка для фамилии учителя (создаем индекс для ускорения поиска)
    last_name = Column(String, index=True)
    # Колонка для должности учителя
    position = Column(String)
    # Колонка для предмета, который преподает учитель
    subject = Column(String)
    exams = relationship("Exam", back_populates="teacher", cascade="all, delete-orphan")

    # Валидация фамилии учителя
    @validates('last_name')
    def validate_last_name(self, key, value):
        """
        Проверяет, что фамилия состоит только из букв (латиница и кириллица) и дефисов.
        Если проверка не пройдена, выбрасывает исключение ValueError.
        """
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё\-]+", value):
            raise ValueError("Фамилия должна состоять только из букв и дефисов")
        return value

    # Валидация должности учителя
    @validates('position')
    def validate_position(self, key, value):
        """
        Проверяет, что должность состоит только из букв (латиница и кириллица) и дефисов.
        Если проверка не пройдена, выбрасывает исключение ValueError.
        """
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё\-]+", value):
            raise ValueError("Должность должна состоять только из букв и дефисов")
        return value

    # Валидация предмета учителя
    @validates('subject')
    def validate_teacher_subject(self, key, value):
        """
        Проверяет, что предмет состоит только из букв (латиница и кириллица) и дефисов.
        Если проверка не пройдена, выбрасывает исключение ValueError.
        """
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё\-]+", value):
            raise ValueError("Предмет должен состоять только из букв и дефисов")
        return value


# Определение модели Exam (Экзамен)
class Exam(Base):
    # Указываем имя таблицы в базе данных
    __tablename__ = "exams"

    # Колонка для уникального идентификатора экзамена (первичный ключ)
    id = Column(Integer, primary_key=True, index=True)
    # Колонка для предмета экзамена (создаем индекс для ускорения поиска)
    subject = Column(String, index=True)
    # Колонка для номера группы, сдающей экзамен
    group_number = Column(String)
    # Колонка для даты проведения экзамена
    exam_date = Column(Date)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False) # nullable=False означает, что teacher_id не может быть пустым
    teacher = relationship("Teacher", back_populates="exams") # back_populates="exams" указывает на обратную связь в модели Teacher

    # Валидация предмета экзамена
    @validates('subject')
    def validate_exam_subject(self, key, value):
        """
        Проверяет, что предмет экзамена состоит только из букв (латиница и кириллица) и дефисов.
        Если проверка не пройдена, выбрасывает исключение ValueError.
        """
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё\-]+", value):
            raise ValueError("Предмет экзамена должен состоять только из букв и дефисов")
        return value

    # Валидация номера группы
    @validates('group_number')
    def validate_group_number(self, key, value):
        """
        Проверяет, что номер группы состоит только из букв, цифр и дефисов.
        Если проверка не пройдена, выбрасывает исключение ValueError.
        """
        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё0-9\-]+", value):
            raise ValueError("Номер группы должен состоять только из букв, цифр и дефисов")
        return value

    # Валидация даты экзамена
    @validates('exam_date')
    def validate_exam_date(self, key, value):
        """
        Проверяет, что дата экзамена не пустая.
        Если проверка не пройдена, выбрасывает исключение ValueError.
        """
        if not value:
            raise ValueError("Дата экзамена не может быть пустой")
        return value