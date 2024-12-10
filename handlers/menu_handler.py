from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from models.base import get_db_session
from models.user_model import User

router = Router()

@router.message(Command("menu"))
async def menu_command(message: Message):
    # Создаём клавиатуру
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📄 Профиль"), KeyboardButton(text="📊 Прогресс")],
            [KeyboardButton(text="🍴 Рекомендации"), KeyboardButton(text="⚙️ Изменить данные")],
            [KeyboardButton(text="❓ Помощь")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Выберите действие:",
        reply_markup=keyboard
    )

# Обработка кнопки "📄 Профиль"
@router.message(lambda message: message.text == "📄 Профиль")
async def show_profile(message: Message):
    telegram_id = message.from_user.id

    # Извлекаем данные пользователя
    with get_db_session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            await message.answer("Ваш профиль не найден. Пожалуйста, зарегистрируйтесь с помощью команды /start.")
            return

        # Отправляем информацию о профиле
        profile_info = (
            f"👤 Ваш профиль:\n\n"
            f"Возраст: {user.age}\n"
            f"Пол: {user.gender}\n"
            f"Рост: {user.height} см\n"
            f"Вес: {user.weight} кг\n"
            f"Цель: {user.goal}"
        )
        await message.answer(profile_info)

# Функция для регистрации обработчиков
def register_menu_handler(dp):
    dp.include_router(router)
