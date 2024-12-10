from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройка базы данных
DATABASE_URL = "sqlite:///diet_bot.db"
engine = create_engine(DATABASE_URL, echo=False)

# Базовый класс для моделей
Base = declarative_base()

# Настройка фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для создания новой сессии
def get_db_session():
    return SessionLocal()
