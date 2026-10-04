import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


load_dotenv()



llm = ChatOpenAI(
    model="qwen/qwen3.8-27b:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    max_tokens=1000,
)

messages = [
    SystemMessage(content="Ты лаконичный технический ассистент!"),
    HumanMessage(content="Назови 3 главных компонента экосистемы LangChain в одно предложение.")
]


print("Отправка тестового запроса...")
response = llm.invoke(messages)

print("\n--ОТВЕТ МОДЕЛИ--")
print(response.content)

print("---------------------")
print("ЗАПРОС УСПЕШНО ВЫПОЛНЕН!")