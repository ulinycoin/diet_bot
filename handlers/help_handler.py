from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

# Создаём экземпляр Router
router = Router()

@router.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "🤖 *Справка по командам бота:*\n\n"
        "\\/start \\- Регистрация или повторное приветствие\n"
        "\\/profile \\- Посмотреть данные вашего профиля\n"
        "\\/edit\\_profile \\- Изменить данные профиля \\(возраст, пол, рост, вес, цель\\)\n"
        "\\/recommend \\- Получить персональные рекомендации по питанию\n"
        "\\/progress \\- Добавить текущий вес и посмотреть динамику\n"
        "\\/clear\\_data \\- Удалить все данные пользователя \\(с подтверждением\\)\n"
        "\\/ask\\_gpt \\- Задать вопрос о питании и получить ответ от ChatGPT\n"
        "\\/help \\- Показать это сообщение\n\n"
        "Если у вас есть вопросы, просто используйте нужную команду или напишите мне\\!"
    )

    # Отправляем текст с MarkdownV2
    await message.answer(help_text, parse_mode="MarkdownV2")

# Регистрация маршрута
def register_help_handler(dp):
    dp.include_router(router)
