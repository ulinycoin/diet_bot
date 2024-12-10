import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from models.base import Base, engine  # Импортируем Base и engine из модели базы данных
from models.user_model import User  # Импортируем вашу модель User

# Создаём таблицы в базе данных, если их ещё нет
def init_db():
    Base.metadata.create_all(bind=engine)
    print("База данных инициализирована.")

if __name__ == "__main__":
    init_db()
