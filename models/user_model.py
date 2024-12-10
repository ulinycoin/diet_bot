from sqlalchemy import Column, Integer, String
from models.base import Base  # Убедитесь, что Base импортируется из models.base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)  # Изменено на Integer
    first_name = Column(String, nullable=True)  # Поле first_name
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    height = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    goal = Column(String, nullable=True)
