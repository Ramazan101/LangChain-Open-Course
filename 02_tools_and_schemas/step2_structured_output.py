import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Загрузка переменных окружения
load_dotenv()

# 2. Инициализация модели через OpenRouter
llm = ChatOpenAI(
    model="qwen/qwen3.8-27b:free",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.2,  # для структурированных данных температуру лучше держать ниже
    max_tokens=1000
)

# 3. Описание схемы выходных данных через Pydantic
class TechnologyAnalysis(BaseModel):
    """Схема структурированного анализа технологии или архитектурного паттерна."""
    name: str = Field(description="Название технологии или паттерна")
    summary: str = Field(description="Краткое описание назначения (1-2 предложения)")
    pros: List[str] = Field(description="Список из 2-3 ключевых преимуществ")
    cons: List[str] = Field(description="Список из 1-2 недостатков или ограничений")
    recommended_use_case: str = Field(description="Идеальный сценарий применения")

# 4. Привязка схемы к модели через with_structured_output
structured_llm = llm.with_structured_output(TechnologyAnalysis)

# 5. Шаблон промпта
prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты senior-архитектор. Проведи объективный технический анализ указанной технологии."),
    ("human", "Проанализируй следующую технологию: {technology}")
])

# 6. Сборка цепочки через LCEL
chain = prompt | structured_llm

# 7. Запуск цепочки
target_tech = "Redis"
print(f"Запуск анализа для: {target_tech}...\n")

result: TechnologyAnalysis = chain.invoke({"technology": target_tech})

# 8. Работа с результатом как с обычным Python-объектом
print("--- РЕЗУЛЬТАТ: ВАЛИДИРОВАННЫЙ ОБЪЕКТ PYDANTIC ---")
print(f"Тип объекта: {type(result)}")
print(f"Технология : {result.name}")
print(f"Описание   : {result.summary}")
print(f"Плюсы      : {', '.join(result.pros)}")
print(f"Минусы     : {', '.join(result.cons)}")
print(f"Сценарий   : {result.recommended_use_case}")
print("-------------------------------------------------")