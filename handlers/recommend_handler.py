from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from models.base import get_db_session
from models.user_model import User

router = Router()

# Команда /recommend — рекомендации по питанию
@router.message(Command("recommend"))
async def recommend_command(message: Message):
    telegram_id = message.from_user.id

    # Получаем данные пользователя из базы
    with get_db_session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            await message.answer("Ваш профиль не найден. Используйте /start для регистрации.")
            return

        # Рассчитываем норму калорий и БЖУ
        calories, protein, fats, carbs = calculate_nutrition(user)

        # Формируем текст с рекомендациями
        recommendation = (
            f"📋 Рекомендации по питанию:\n\n"
            f"🍎 Дневная норма калорий: {calories} ккал\n"
            f"💪 Белки: {protein} г\n"
            f"🥑 Жиры: {fats} г\n"
            f"🍞 Углеводы: {carbs} г\n\n"
            f"Примерный рацион:\n"
            f"- Завтрак: овсянка с фруктами и орехами\n"
            f"- Обед: куриная грудка, рис и овощи\n"
            f"- Ужин: рыба с запечёнными овощами\n"
            f"- Перекусы: орехи, йогурт или фрукты\n"
        )
        await message.answer(recommendation)

# Функция для расчёта дневной нормы калорий и БЖУ
def calculate_nutrition(user):
    # Формулы расчёта калорий
    if user.gender == "мужской":
        bmr = 88.36 + (13.4 * user.weight) + (4.8 * user.height) - (5.7 * user.age)
    else:
        bmr = 447.6 + (9.2 * user.weight) + (3.1 * user.height) - (4.3 * user.age)

    # Уровень активности
    activity_multiplier = {
        "low": 1.2,
        "medium": 1.55,
        "high": 1.75
    }.get(user.activity_level, 1.2)

    # Калории с учётом активности
    calories = int(bmr * activity_multiplier)

    # Корректировка для целей
    if user.goal == "похудение":
        calories -= 500
    elif user.goal == "набор массы":
        calories += 500

    # Распределение БЖУ
    protein = int(0.3 * calories / 4)  # 30% калорийности
    fats = int(0.25 * calories / 9)    # 25% калорийности
    carbs = int(0.45 * calories / 4)   # 45% калорийности

    return calories, protein, fats, carbs

# Регистрация маршрута
def register_recommend_handler(dp):
    dp.include_router(router)
