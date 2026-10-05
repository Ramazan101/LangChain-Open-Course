import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, Runnable

# 1. Загрузка переменных окружения.
load_dotenv()

# 2. Инициализация модели через OpenRouter.
llm = ChatOpenAI(
    model="qwen/qwen3.8-27b:free",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.2,
    max_tokens=2000,
)

# 3. Описание схемы выхода данных через Pydantic.
class AnswerOutputSchema(BaseModel):
    """Вывод ответа через Pydantic."""
    name: str = Field(description="Имя запроса или данные переданные в модель.")
    answer: str = Field(description="Ответ модельки на вопрос пользователя.")
    datetime: datetime #= Field(description="Точное время ответа модельки.")


# 4. Привязка схемы к модели через with_structured_output.
structured_llm = llm.with_structured_output(AnswerOutputSchema)


# 5. Шаблон промпта для LLM.
prompt = ChatPromptTemplate([
    ("system", "Ты senior Python Developer. Отвечай четко и коротко с примерами."),
    ("human", "Проанализируй следующий запрос: {text}")
])


# 6. Сборка цепочки через LCEL.
chain = prompt | structured_llm

# 7. Запуск цепочки.
input_text = "что такое инкапсуляция?"
print(f"Запуск анализа для {input_text}...\n")

result: AnswerOutputSchema = chain.invoke({"text": input_text})

print("---ВЫВОД ВАЛИДИРОВАННЫХ ДАННЫХ НА КОНСОЛЬ---")
print(f"Тип ответа: {type(result)}")
print(f"Контекст: {result.name}")
print(f"Ответ: {result.answer}")
print(f"Время ответа: {result.datetime}")
print("--------------------------------------------")