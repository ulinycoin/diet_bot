from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from datetime import datetime
from models.base import get_db_session
from models.user_model import User
from models.progress_model import Progress

router = Router()

# Определяем состояния для FSM
class ProgressState(StatesGroup):
    waiting_for_weight = State()

@router.message(Command("progress"))
async def progress_command(message: Message, state: FSMContext):
    telegram_id = message.from_user.id

    # Проверяем, зарегистрирован ли пользователь
    with get_db_session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            await message.answer("Ваш профиль не найден. Используйте /start для регистрации.")
            return

    # Запрашиваем текущий вес
    await message.answer("Введите ваш текущий вес в килограммах:")
    await state.set_state(ProgressState.waiting_for_weight)

@router.message(ProgressState.waiting_for_weight)
async def save_progress(message: Message, state: FSMContext):
    # Получаем вес
    try:
        weight = float(message.text)
        if weight <= 0:
            raise ValueError("Некорректный вес.")
    except ValueError:
        await message.answer("Пожалуйста, введите корректный вес (например, 70.5).")
        return

    telegram_id = message.from_user.id
    current_time = datetime.now()  # Текущее время

    with get_db_session() as session:
        # Получаем пользователя
        user = session.query(User).filter_by(telegram_id=telegram_id).first()

        if not user:
            await message.answer("Ваш профиль не найден. Используйте /start для регистрации.")
            return

        # Сохраняем текущий вес
        progress = Progress(user_id=user.id, weight=weight, date=current_time)
        session.add(progress)
        session.commit()

        # Получаем предыдущую запись (исключая текущую)
        previous_progress = (
            session.query(Progress)
            .filter(Progress.user_id == user.id, Progress.date < current_time)
            .order_by(Progress.date.desc())
            .first()
        )

    # Рассчитываем изменения
    if previous_progress:
        weight_diff = weight - previous_progress.weight
        trend = "снизился" if weight_diff < 0 else "увеличился"
        diff_text = f"Ваш вес {trend} на {abs(weight_diff):.1f} кг с последнего измерения."
    else:
        diff_text = "Это ваша первая запись о весе."

    # Отправляем отчёт
    await message.answer(
        f"Текущий вес: {weight:.1f} кг\n"
        f"{diff_text}\n\n"
        f"Продолжайте отслеживать ваш прогресс!"
    )
    await state.clear()


# Регистрация маршрута
def register_progress_handler(dp):
    dp.include_router(router)
