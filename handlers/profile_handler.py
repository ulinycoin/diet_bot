from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from models.base import get_db_session
from models.user_model import User

router = Router()

@router.message(Command("profile"))
async def view_profile(message: Message):
    telegram_id = message.from_user.id

    # Получаем данные пользователя из базы данных
    with get_db_session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()

        if not user:
            await message.answer("Ваш профиль не найден. Используйте /start для регистрации.")
            return

        # Формируем текст с данными профиля
        profile_text = (
            f"👤 Ваш профиль:\n"
            f"Возраст: {user.age}\n"
            f"Пол: {user.gender.capitalize()}\n"
            f"Рост: {user.height} см\n"
            f"Вес: {user.weight} кг\n"
            f"Цель: {user.goal.capitalize()}"
        )
        await message.answer(profile_text)

# Регистрация маршрута
def register_profile_handler(dp):
    dp.include_router(router)
