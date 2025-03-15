from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Определение URL для подключения к базе данных PostgreSQL
DATABASE_URL = "postgresql://postgres:0aCX70TYQW3R@postgres:5432/postgres"
engine = create_engine(DATABASE_URL)
# - autocommit=False: автоматическое подтверждение изменений отключено (требуется явный вызов commit), autoflush=False: автоматическая синхронизация сессии с базой данных отключена, bind=engine: привязка сессий к созданному движку
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса для моделей SQLAlchemy
# Все модели (таблицы) будут наследоваться от этого класса
Base = declarative_base()