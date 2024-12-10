from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models.base import get_db_session
from models.user_model import User
from models.progress_model import Progress

router = Router()

# Команда /clear_data
@router.message(Command("clear_data"))
async def clear_data_command(message: Message):
    # Отправляем пользователю запрос на подтверждение
    confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, удалить данные", callback_data="confirm_clear_data")],
        [InlineKeyboardButton(text="Нет, оставить всё как есть", callback_data="cancel_clear_data")]
    ])
    await message.answer(
        "Вы уверены, что хотите удалить все ваши данные из базы? Это действие необратимо.",
        reply_markup=confirm_keyboard
    )

# Обработка подтверждения удаления
@router.callback_query(lambda c: c.data == "confirm_clear_data")
async def confirm_clear_data(callback: CallbackQuery):
    telegram_id = callback.from_user.id

    # Удаляем данные пользователя из базы
    with get_db_session() as session:
        # Удаляем записи из таблицы прогресса
        session.query(Progress).filter_by(user_id=telegram_id).delete()

        # Удаляем профиль пользователя
        session.query(User).filter_by(telegram_id=telegram_id).delete()
        session.commit()

    # Уведомляем пользователя об успешном удалении
    await callback.message.edit_text("Все ваши данные успешно удалены из базы. Если понадобится, вы можете зарегистрироваться заново с помощью /start.")

# Обработка отмены удаления
@router.callback_query(lambda c: c.data == "cancel_clear_data")
async def cancel_clear_data(callback: CallbackQuery):
    await callback.message.edit_text("Данные не были удалены. Вы можете продолжать пользоваться ботом.")

# Регистрация маршрута
def register_clear_data_handler(dp):
    dp.include_router(router)
