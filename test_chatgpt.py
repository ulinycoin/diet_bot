from services.chatgpt_service import ask_gpt

if __name__ == "__main__":
    question = input("Введите ваш вопрос для ChatGPT: ")
    answer = ask_gpt(question)
    print(f"Ответ от ChatGPT:\n{answer}")
