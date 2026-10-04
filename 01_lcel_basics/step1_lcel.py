import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1.Загрузка переменных окружения
load_dotenv()

# 2.Инициализация модели через шлюз OpenRouter
llm = ChatOpenAI(
    model="qwen/qwen3.8-27b:free",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.7,
)

# 3.Шаблон промпта с плейсхолдерами
prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты опытный Python-разработчик. Объясняй концепции кратко, ёмко и с одним примером кода."),
    ("human", "Что такое {topic} в контексте {domain} и зачем это нужно?")
])


# 4.Парсер вывода (преобразует AIMessage напрямую в str)
parser = StrOutputParser()

# 5.Сборка цепочки через LCEL (пайплайн)
chain = prompt | llm | parser


# 6.Запуск выполнение цепочки
inputs = {
    "topic": "паттерн Singleton",
    "domain": "архитектуры ПО"
}

print(f"Запуск цепочки LCEL для темы: '{inputs['topic']}'...\n")
result = chain.invoke(inputs)

print("--- РЕЗУЛЬТАТ (чистый str) ---")
print(result)
print("------------------------------")