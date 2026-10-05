import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 1. Загрузка переменных окружения.
load_dotenv() # здесь было ошибка при первом запуске. Не сработала
              # site-pages 'python-dotenv'!...


# 2. Инициализации модели через OpenRouter.
llm = ChatOpenAI(
    model="qwen/qwen3.8-27b:free", # Бесплатный модель от OpenAI. Есть другие...
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    max_tokens=1000,
)


# 3. Шаблон промпта.
messages = [
    SystemMessage(content="Ты лаконичный технический ассистент!"),
    HumanMessage(content="Назови 3 главных компонента экосистемы LangChain в одно предложение.")
]

# 4. Запуск llm - 'models: qwen/free'
print("Отправка тестового запроса...")
response = llm.invoke(messages)

print("\n--ОТВЕТ МОДЕЛИ--")
print(response.content)

print("---------------------")
print("ЗАПРОС УСПЕШНО ВЫПОЛНЕН!")