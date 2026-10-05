import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

# 1. Загрузка переменных окружения
load_dotenv()

# 2. Инициализация модели через OpenRouter
llm = ChatOpenAI(
    model="qwen/qwen3.8-27b:free",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0,  # нулевая температура обязательна для детерминированного вызова функций
)

# 3. Объявление кастомного инструмента с помощью декоратора @tool
@tool
def calculate_server_cost(instances: int, hours: int, price_per_hour: float = 0.05) -> float:
    """Рассчитывает общую стоимость аренды серверов в облаке.

    Args:
        instances: Количество виртуальных машин.
        hours: Время работы серверов в часах.
        price_per_hour: Цена за один сервер в час (по умолчанию 0.05).
    """
    return round(instances * hours * price_per_hour, 2)

# 4. Привязка списка доступных инструментов к модели
tools = [calculate_server_cost]
tools_by_name = {t.name: t for t in tools}
llm_with_tools = llm.bind_tools(tools)

# 5. Формирование запроса пользователя
user_prompt = "Сколько будет стоить аренда 6 серверов на 150 часов при стандартном тарифе?"
messages = [HumanMessage(content=user_prompt)]

print(f"Вопрос: {user_prompt}\n")
print("Шаг 1: Запрос к модели для определения инструмента...")

# Первый вызов: модель анализирует задачу
ai_response = llm_with_tools.invoke(messages)
messages.append(ai_response)

print("\n--- СЫРОЙ ОТВЕТ МОДЕЛИ ---")
print(f"Tool calls: {ai_response.tool_calls}")
print("---------------------------\n")

# 6. Обработка и локальное выполнение вызовов инструментов
if ai_response.tool_calls:
    for tool_call in ai_response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]

        print(f"Выполнение инструмента '{tool_name}' с параметрами {tool_args}...")

        # Запуск функции через реестр
        tool_function = tools_by_name[tool_name]
        tool_output = tool_function.invoke(tool_args)

        print(f" Результат выполнения: {tool_output}")

        # Формирование ToolMessage с привязкой к ID вызова
        messages.append(
            ToolMessage(
                content=str(tool_output),
                tool_call_id=tool_id
            )
        )

    # 7. Второй вызов: генерация финального ответа на основе данных от инструмента
    print("\nШаг 2: Модель синтезирует итоговый ответ с учетом вычислений...")
    final_response = llm_with_tools.invoke(messages)

    print("\n--- ИТОГОВЫЙ ОТВЕТ ---")
    print(final_response.content)
    print("----------------------")
else:
    print("Модель ответила напрямую без вызова инструментов:")
    print(ai_response.content)