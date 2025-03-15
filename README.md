Это веб-приложение для управления данными об учителях и экзаменах. Оно построено на базе FastAPI, SQLAlchemy и PostgreSQL. Приложение предоставляет REST API для работы с данными и веб-интерфейс для удобного взаимодействия.

1) Технологии
- Backend: FastAPI
- База данных: PostgreSQL
- ORM: SQLAlchemy
- Фронтенд: HTML, CSS, JavaScript
- Контейнеризация: Docker 

2) Требования
- Python 3.9 или выше
- PostgreSQL
- Docker 

3)Установка и запуск

1. Клонирование репозитория
Склонируйте репозиторий на ваш компьютер:
git clone https://github.com/Kokur1n/KURSA4/
cd KURSA4


2. Настройка виртуального окружения
Создайте виртуальное окружение и установите зависимости:
python -m venv venv
source venv/bin/activate  (Для Linux/MacOS)
venv\Scripts\activate (для Windows)


pip install -r requirements.txt

3. Запуск приложения
Запустите FastAPI-приложение:
uvicorn main:app --reload
Приложение будет доступно по адресу: http://127.0.0.1:8000

4. Запуск через Docker 
Если вы хотите запустить проект через Docker, выполните следующие шаги:
1. Убедитесь, что у вас установлен Docker и Docker Compose.
2. Соберите и запустите контейнеры:
   docker-compose up --build
   Приложение будет доступно по адресу: [http://localhost:9532
