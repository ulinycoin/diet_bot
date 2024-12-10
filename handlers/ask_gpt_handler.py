from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.chatgpt_service import ask_gpt
from models.base import get_db_session
from models.user_model import User

router = Router()

# Максимальная длина сообщения Telegram
TELEGRAM_MESSAGE_LIMIT = 4096

def split_message(text, limit=TELEGRAM_MESSAGE_LIMIT):
    """
    Делит текст на части, если он превышает лимит символов.
    :param text: Исходный текст
    :param limit: Максимальная длина одной части
    :return: Список частей
    """
    parts = []
    while len(text) > limit:
        # Находим последний пробел перед лимитом
        split_index = text[:limit].rfind(' ')
        if split_index == -1:  # Если пробела нет, режем строго по лимиту
            split_index = limit
        parts.append(text[:split_index])
        text = text[split_index:].strip()
    parts.append(text)  # Добавляем оставшуюся часть
    return parts

@router.message(Command("ask_gpt"))
async def ask_gpt_command(message: Message):
    telegram_id = message.from_user.id

    # Извлекаем данные пользователя из базы
    with get_db_session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            await message.answer("Ваш профиль не найден. Сначала зарегистрируйтесь с помощью команды /start.")
            return

        # Формируем контекст из данных пользователя
        user_context = (
            f"Возраст: {user.age}\n"
            f"Пол: {user.gender}\n"
            f"Рост: {user.height} см\n"
            f"Вес: {user.weight} кг\n"
            f"Цель: {user.goal}\n\n"
        )

    # Запрашиваем вопрос у пользователя
    await message.answer("Напишите ваш вопрос, и я постараюсь вам помочь с учётом ваших данных.")

    # Ждём вопрос
    @router.message()
    async def process_question(user_message: Message):
        question = user_message.text
        prompt = (
            f"Вот данные пользователя:\n{user_context}\n"
            f"Вопрос пользователя: {question}\n\n"
            f"Ответь как профессиональный диетолог, учитывая эти данные."
        )

        # Отправляем запрос в ChatGPT
        await user_message.answer("Секунду, я обрабатываю ваш запрос...")
        answer = ask_gpt(prompt)

        # Отправляем ответ частями, если он длинный
        for part in split_message(answer):
            await user_message.answer(part)


# Регистрация маршрута
def register_ask_gpt_handler(dp):
    dp.include_router(router)
