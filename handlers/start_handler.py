from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from models.base import get_db_session
from models.user_model import User

router = Router()

# Состояния для регистрации
class RegistrationStates(StatesGroup):
    age = State()
    gender = State()
    height = State()
    weight = State()
    goal = State()

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    first_name = message.from_user.first_name

    # Проверяем, есть ли пользователь в базе
    with get_db_session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            await message.answer(f"Добро пожаловать обратно, {first_name}!")
        else:
            # Запускаем регистрацию
            await message.answer("Добро пожаловать! Давайте начнём регистрацию.")
            await message.answer("Введите ваш возраст:")
            await state.set_state(RegistrationStates.age)

@router.message(RegistrationStates.age)
async def process_age(message: Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer("Пожалуйста, введите число.")
        return
    await state.update_data(age=int(age))
    await message.answer("Введите ваш пол (м/ж):")
    await state.set_state(RegistrationStates.gender)

@router.message(RegistrationStates.gender)
async def process_gender(message: Message, state: FSMContext):
    gender = message.text.lower()
    if gender not in ["м", "ж"]:
        await message.answer("Пожалуйста, укажите 'м' или 'ж'.")
        return
    await state.update_data(gender=gender)
    await message.answer("Введите ваш рост в сантиметрах:")
    await state.set_state(RegistrationStates.height)

@router.message(RegistrationStates.height)
async def process_height(message: Message, state: FSMContext):
    height = message.text
    if not height.isdigit():
        await message.answer("Пожалуйста, введите число.")
        return
    await state.update_data(height=int(height))
    await message.answer("Введите ваш вес в килограммах:")
    await state.set_state(RegistrationStates.weight)

@router.message(RegistrationStates.weight)
async def process_weight(message: Message, state: FSMContext):
    weight = message.text
    if not weight.isdigit():
        await message.answer("Пожалуйста, введите число.")
        return
    await state.update_data(weight=int(weight))
    await message.answer("Какова ваша цель? (похудение/набор веса/поддержание формы):")
    await state.set_state(RegistrationStates.goal)

@router.message(RegistrationStates.goal)
async def process_goal(message: Message, state: FSMContext):
    goal = message.text.lower()
    if goal not in ["похудение", "набор веса", "поддержание формы"]:
        await message.answer("Пожалуйста, укажите одну из целей: похудение, набор веса, поддержание формы.")
        return

    # Сохраняем данные пользователя
    user_data = await state.get_data()
    with get_db_session() as session:
        new_user = User(
            telegram_id=message.from_user.id,
            first_name=message.from_user.first_name,
            age=user_data["age"],
            gender=user_data["gender"],
            height=user_data["height"],
            weight=user_data["weight"],
            goal=goal,
        )
        session.add(new_user)
        session.commit()

    await message.answer("Регистрация завершена! Вы можете воспользоваться ботом для отслеживания прогресса и получения рекомендаций.")

    # Отправляем клавиатуру с меню
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📄 Профиль"), KeyboardButton(text="📊 Прогресс")],
            [KeyboardButton(text="🍴 Рекомендации"), KeyboardButton(text="⚙️ Изменить данные")],
            [KeyboardButton(text="❓ Помощь")]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите действие из меню ниже:", reply_markup=keyboard)

    # Сбрасываем состояние
    await state.clear()

# Регистрация маршрута
def register_start_handler(dp):
    dp.include_router(router)
