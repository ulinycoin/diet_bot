from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from models.base import get_db_session
from models.user_model import User

router = Router()

# Состояния для редактирования профиля
class EditProfileStates(StatesGroup):
    field = State()
    value = State()

# Команда /edit_profile — начало редактирования
@router.message(Command("edit_profile"))
async def edit_profile_start(message: Message, state: FSMContext):
    telegram_id = message.from_user.id

    # Проверяем, существует ли пользователь
    with get_db_session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            await message.answer("Ваш профиль не найден. Используйте /start для регистрации.")
            return

    await message.answer(
        "Что вы хотите изменить?\n"
        "Доступные поля: возраст, пол, рост, вес, цель."
    )
    await state.set_state(EditProfileStates.field)

# Шаг 1: Пользователь указывает поле для редактирования
@router.message(EditProfileStates.field)
async def choose_field(message: Message, state: FSMContext):
    field = message.text.lower()
    valid_fields = {"возраст": "age", "пол": "gender", "рост": "height", "вес": "weight", "цель": "goal"}

    if field not in valid_fields:
        await message.answer("Неверное поле. Выберите одно из: возраст, пол, рост, вес, цель.")
        return

    # Сохраняем выбранное поле
    await state.update_data(field=valid_fields[field])
    await message.answer(f"Введите новое значение для {field}.")
    await state.set_state(EditProfileStates.value)

# Шаг 2: Пользователь указывает новое значение
@router.message(EditProfileStates.value)
async def update_value(message: Message, state: FSMContext):
    new_value = message.text
    data = await state.get_data()

    field = data["field"]
    telegram_id = message.from_user.id

    # Проверка корректности ввода для конкретного поля
    if field in {"age", "height", "weight"} and not new_value.isdigit():
        await message.answer("Значение должно быть числом. Попробуйте ещё раз.")
        return

    if field == "gender" and new_value.lower() not in {"мужской", "женский"}:
        await message.answer("Пол может быть только 'мужской' или 'женский'. Попробуйте ещё раз.")
        return

    if field == "goal" and new_value.lower() not in {"похудение", "набор массы", "поддержание веса"}:
        await message.answer("Цель может быть только 'похудение', 'набор массы' или 'поддержание веса'. Попробуйте ещё раз.")
        return

    # Приведение данных к нужному типу
    if field in {"age", "height", "weight"}:
        new_value = int(new_value)

    # Обновление данных в базе
    with get_db_session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        setattr(user, field, new_value)
        session.commit()

    await message.answer(f"Ваше поле {field} успешно обновлено!")
    await state.clear()

# Регистрация маршрута
def register_edit_profile_handler(dp):
    dp.include_router(router)
