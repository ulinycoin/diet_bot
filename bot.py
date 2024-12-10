import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers.start_handler import register_start_handler
from handlers.profile_handler import register_profile_handler
from handlers.edit_profile_handler import register_edit_profile_handler
from handlers.recommend_handler import register_recommend_handler
from handlers.help_handler import register_help_handler
from handlers.progress_handler import register_progress_handler
from handlers.clear_data_handler import register_clear_data_handler
from handlers.ask_gpt_handler import register_ask_gpt_handler
from handlers.menu_handler import register_menu_handler


# Создаем экземпляр бота
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация всех обработчиков
def register_handlers():
    register_start_handler(dp)
    register_profile_handler(dp)
    register_edit_profile_handler(dp)
    register_recommend_handler(dp)
    register_help_handler(dp)
    register_progress_handler(dp)
    register_clear_data_handler(dp)
    register_ask_gpt_handler(dp)
    register_menu_handler(dp)

async def main():
    print("Бот запущен...")
    register_handlers()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
