from fastapi import FastAPI, HTTPException, Depends, Request  # FastAPI для создания API, HTTPException для обработки ошибок, Depends для зависимостей
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session  # Session для работы с сессиями базы данных
from starlette.responses import RedirectResponse  # RedirectResponse для перенаправления запросов
from starlette.staticfiles import StaticFiles  # StaticFiles для обслуживания статических файлов
from typing import List, Dict, Any  # Типы данных для аннотаций
import models  # Модуль с моделями базы данных
import schemas  # Модуль с Pydantic схемами для валидации данных
import crud  # Модуль с функциями для работы с базой данных (CRUD операции)
from database import SessionLocal, engine  # SessionLocal для создания сессий, engine для подключения к базе данных

# Создание таблиц в базе данных на основе моделей
models.Base.metadata.create_all(bind=engine)

# Создание экземпляра FastAPI приложения
app = FastAPI()

# Монтирование статических файлов (например, HTML, CSS, JS) по пути "/static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Функция-зависимость для получения сессии базы данных
def get_db():
    # Создание новой сессии базы данных
    db = SessionLocal()
    try:
        # Возврат сессии для использования в запросе
        yield db
    finally:
        # Закрытие сессии после завершения запроса
        db.close()
        
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )
# Корневой эндпоинт, который перенаправляет на статическую страницу index.html
@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

# --- Эндпоинты для работы с учителями (Teacher) ---

# Эндпоинт для получения списка всех учителей
@app.get(
    "/teachers/",
    response_model=List[schemas.Teacher],  # Указываем модель ответа (список учителей)
    summary="Получить список учителей",  # Краткое описание эндпоинта
    description="Возвращает список всех учителей, зарегистрированных в базе данных."  # Подробное описание
)
def read_teachers(db: Session = Depends(get_db)):
    """
    Получить список всех учителей.
    """
    # Вызов функции из модуля crud для получения списка учителей
    return crud.get_teachers(db)

# Эндпоинт для получения информации о конкретном учителе по его ID
@app.get(
    "/teachers/{teacher_id}",
    response_model=schemas.Teacher,  # Модель ответа (один учитель)
    summary="Получить учителя",  # Краткое описание
    description="Возвращает информацию о конкретном учителе по его ID."  # Подробное описание
)
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    """
    Получить данные конкретного учителя по идентификатору.
    """
    # Получение учителя из базы данных по ID
    db_teacher = crud.get_teacher(db, teacher_id)
    # Если учитель не найден, возвращаем ошибку 404
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Учитель не найден")
    # Возвращаем данные учителя
    return db_teacher

# Эндпоинт для создания нового учителя
@app.post(
    "/teachers/",
    response_model=schemas.Teacher,  # Модель ответа (созданный учитель)
    summary="Создать нового учителя",  # Краткое описание
    description="Создает нового учителя с указанными данными и сохраняет его в базе данных."  # Подробное описание
)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    """
    Создать нового учителя.
    """
    # Вызов функции из модуля crud для создания учителя
    return crud.create_teacher(db, teacher)

# Эндпоинт для обновления данных учителя по его ID
@app.put(
    "/teachers/{teacher_id}",
    response_model=schemas.Teacher,  # Модель ответа (обновленный учитель)
    summary="Обновить данные учителя",  # Краткое описание
    description="Обновляет данные существующего учителя по его ID."  # Подробное описание
)
def update_teacher(
    teacher_id: int, teacher: schemas.TeacherCreate, db: Session = Depends(get_db)
):
    """
    Обновить данные учителя.
    """
    # Вызов функции из модуля crud для обновления данных учителя
    db_teacher = crud.update_teacher(db, teacher_id, teacher)
    # Если учитель не найден, возвращаем ошибку 404
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Учитель не найден")
    # Возвращаем обновленные данные учителя
    return db_teacher

# Эндпоинт для удаления учителя по его ID
@app.delete(
    "/teachers/{teacher_id}",
    response_model=schemas.Teacher,  # Модель ответа (удаленный учитель)
    summary="Удалить учителя",  # Краткое описание
    description="Удаляет учителя по его ID из базы данных."  # Подробное описание
)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    """
    Удалить учителя.
    """
    # Вызов функции из модуля crud для удаления учителя
    db_teacher = crud.delete_teacher(db, teacher_id)
    # Если учитель не найден, возвращаем ошибку 404
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Учитель не найден")
    # Возвращаем данные удаленного учителя
    return db_teacher

# --- Эндпоинты для работы с экзаменами (Exams) ---

# Эндпоинт для получения списка всех экзаменов
@app.get(
    "/exams/",
    response_model=List[schemas.Exam],  # Модель ответа (список экзаменов)
    summary="Получить список экзаменов",  # Краткое описание
    description="Возвращает список всех экзаменов, зарегистрированных в базе данных."  # Подробное описание
)
def read_exams(db: Session = Depends(get_db)):
    """
    Получить список всех экзаменов.
    """
    # Вызов функции из модуля crud для получения списка экзаменов
    return crud.get_exams(db)

# Эндпоинт для получения информации о конкретном экзамене по его ID
@app.get(
    "/exams/{exam_id}",
    response_model=schemas.Exam,  # Модель ответа (один экзамен)
    summary="Получить экзамен",  # Краткое описание
    description="Возвращает информацию о конкретном экзамене по его ID."  # Подробное описание
)
def read_exam(exam_id: int, db: Session = Depends(get_db)):
    """
    Получить данные конкретного экзамена.
    """
    # Получение экзамена из базы данных по ID
    db_exam = crud.get_exam(db, exam_id)
    # Если экзамен не найден, возвращаем ошибку 404
    if db_exam is None:
        raise HTTPException(status_code=404, detail="Экзамен не найден")
    # Возвращаем данные экзамена
    return db_exam

# Эндпоинт для создания нового экзамена
@app.post(
    "/exams/",
    response_model=schemas.Exam,  # Модель ответа (созданный экзамен)
    summary="Создать новый экзамен",  # Краткое описание
    description="Создает новый экзамен с указанными данными и сохраняет его в базе данных."  # Подробное описание
)
def create_exam(exam: schemas.ExamCreate, db: Session = Depends(get_db)):
    """
    Создать новый экзамен.
    """
    # Вызов функции из модуля crud для создания экзамена
    return crud.create_exam(db, exam)

# Эндпоинт для обновления данных экзамена по его ID
@app.put(
    "/exams/{exam_id}",
    response_model=schemas.Exam,  # Модель ответа (обновленный экзамен)
    summary="Обновить данные экзамена",  # Краткое описание
    description="Обновляет данные существующего экзамена по его ID."  # Подробное описание
)
def update_exam(
    exam_id: int, exam: schemas.ExamCreate, db: Session = Depends(get_db)
):
    """
    Обновить данные экзамена.
    """
    # Вызов функции из модуля crud для обновления данных экзамена
    db_exam = crud.update_exam(db, exam_id, exam)
    # Если экзамен не найден, возвращаем ошибку 404
    if db_exam is None:
        raise HTTPException(status_code=404, detail="Экзамен не найден")
    # Возвращаем обновленные данные экзамена
    return db_exam

# Эндпоинт для удаления экзамена по его ID
@app.delete(
    "/exams/{exam_id}",
    response_model=schemas.Exam,  # Модель ответа (удаленный экзамен)
    summary="Удалить экзамен",  # Краткое описание
    description="Удаляет экзамен по его ID из базы данных."  # Подробное описание
)
def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    """
    Удалить экзамен.
    """
    # Вызов функции из модуля crud для удаления экзамена
    db_exam = crud.delete_exam(db, exam_id)
    # Если экзамен не найден, возвращаем ошибку 404
    if db_exam is None:
        raise HTTPException(status_code=404, detail="Экзамен не найден")
    # Возвращаем данные удаленного экзамена
    return db_exam

# Эндпоинт для получения экзаменов, связанных с конкретным учителем
@app.get(
    "/teachers/{teacher_id}/exams/",
    response_model=schemas.TeacherExams,  # Модель ответа (учитель и его экзамены)
    summary="Получить экзамены учителя",  # Краткое описание
    description=(
        "Возвращает информацию о конкретном учителе и список экзаменов, привязанных к нему."
    ),
)
def get_teacher_exams(teacher_id: int, db: Session = Depends(get_db)):
    # Получение данных учителя и его экзаменов
    teacher, exams = crud.get_teacher_exams(db, teacher_id)
    # Если учитель не найден, возвращаем ошибку 404
    if teacher is None:
        raise HTTPException(status_code=404, detail="Учитель не найден")
    # Возвращаем данные учителя и его экзаменов
    return {"teacher": teacher, "exams": exams}

# Эндпоинт для поиска учителей по фамилии
@app.get(
    "/teachers/search/",
    response_model=List[schemas.Teacher],  # Модель ответа (список учителей)
    summary="Поиск учителей",  # Краткое описание
    description="Возвращает список учителей, фамилия которых соответствует поисковому запросу."  # Подробное описание
)
def search_teacher(q: str, db: Session = Depends(get_db)):
    # Вызов функции из модуля crud для поиска учителей
    return crud.search_teachers(db, q)

# Эндпоинт для поиска экзаменов по предмету
@app.get(
    "/exams/search/",
    response_model=List[schemas.Exam],  # Модель ответа (список экзаменов)
    summary="Поиск экзаменов",  # Краткое описание
    description="Возвращает список экзаменов, предмет которых соответствует поисковому запросу."  # Подробное описание
)
def search_exam(q: str, db: Session = Depends(get_db)):
    # Вызов функции из модуля crud для поиска экзаменов
    return crud.search_exams(db, q)