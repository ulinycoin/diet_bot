import openai
from config import OPENAI_API_KEY

# Устанавливаем API-ключ
openai.api_key = OPENAI_API_KEY

def ask_gpt(prompt: str, model: str = "gpt-3.5-turbo", max_tokens: int = 1000) -> str:
    """
    Отправляет запрос в GPT и возвращает полный ответ.
    Если ответ обрезается, запрашивает продолжение.
    :param prompt: Вопрос для GPT
    :param model: Модель GPT (например, gpt-3.5-turbo или gpt-4)
    :param max_tokens: Максимальное количество токенов в одном запросе
    :return: Полный текст ответа от GPT
    """
    try:
        # Отправляем первый запрос
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        answer = response["choices"][0]["message"]["content"].strip()

        # Проверяем, есть ли необходимость продолжить ответ
        while len(response["choices"][0]["finish_reason"]) == 0 or response["choices"][0]["finish_reason"] == "length":
            # Добавляем контекст продолжения
            prompt = "Продолжи ответ: " + answer.split()[-50:]
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7
            )
            new_answer = response["choices"][0]["message"]["content"].strip()
            answer += " " + new_answer

        return answer
    except Exception as e:
        return f"Произошла ошибка: {e}"
