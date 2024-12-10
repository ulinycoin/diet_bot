from models.base import Base, engine
from models.user_model import User

# Создание таблиц
def init_db():
    Base.metadata.create_all(bind=engine)
    print("База данных инициализирована.")

if __name__ == "__main__":
    init_db()
