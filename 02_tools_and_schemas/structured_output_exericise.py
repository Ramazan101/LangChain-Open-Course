import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

# 1. Загрузка переменных окружения.
load_dotenv()

# 2. Инициализация модели через OpenRouter.
llm = ChatOpenAI(
    model="qwen/qwen3.8-27b:free",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.1,
    max_tokens=1500,
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

# Три функции с помощью RunnableLambda.

# Функция 1: Предобработка текста (удаляет пробелы, приводит к нижнему регистру).
def clean_input(data: dict) -> dict:
    cleaned_text = data.get("text", "").strip().lower()
    return {"text": cleaned_text}

# Функция 2: Логирование / перехват промежуточных данных перед отправкой в LLM.
def log_step(prompt_value):
    print(f"Промпт успешно сформирован {prompt_value.to_messages()[-1].content}")
    return prompt_value

# Функция 3: Постобработка Pydantic-объекта.
def format_output(result: AnswerOutputSchema) -> AnswerOutputSchema:
    result.answer = f"Итоговый ответ сениора: {result.answer}"
    return result


runnable_cleaned = RunnableLambda(clean_input)
runnable_log_step = RunnableLambda(log_step)
runnable_format_output = RunnableLambda(format_output)

# 6. Сборка цепочки через LCEL.
chain = runnable_cleaned | prompt | runnable_log_step | structured_llm | runnable_format_output

# 7. Запуск цепочки.
input_text = "что такое ООП?"
print(f"Запуск анализа для {input_text}...\n")

result: AnswerOutputSchema = chain.invoke({"text": input_text})

print("---ВЫВОД ВАЛИДИРОВАННЫХ ДАННЫХ НА КОНСОЛЬ---")
print(f"Тип ответа: {type(result)}")
print(f"Контекст: {result.name}")
print(f"Ответ: {result.answer}")
print(f"Время ответа: {result.datetime}")
print("--------------------------------------------")