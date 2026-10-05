# Практический курс LangChain и LangGraph

Репозиторий с практическими заданиями по LangChain: цепочки LCEL, структурированный вывод, вызов инструментов, а дальше RAG и агенты на LangGraph. Каждый модуль содержит рабочие скрипты и подробный справочник с терминами, схемами и разбором кода. Справочники написаны так, чтобы их понял новичок, и в то же время содержат технические детали для опытного разработчика.

## Модули

| Модуль | О чём | Файлы | Статус |
| :--- | :--- | :--- | :--- |
| [00_setup](00_setup/README.md) | Окружение, ключи, OpenRouter, первый вызов модели | `test_setup.py`, `number_two_test_setup.py` | готово |
| [01_lcel_basics](01_lcel_basics/README.md) | Цепочки через оператор «\|», шаблоны, парсер | `step1_lcel.py` | готово |
| [02_tools_and_schemas](02_tools_and_schemas/README.md) | Схемы Pydantic и вызов инструментов | `step2_structured_output.py`, `structured_output_exericise.py`, `step3_tool_calling.py` | готово |
| 03_rag_vectorstores | Хранилища векторов и поиск по контексту | — | запланировано |
| 04_langgraph_agents | Циклы, состояние и мультиагентные системы | — | запланировано |

## Структура репозитория

```text
LangChain-Open-Course/
├── 00_setup/
│   ├── test_setup.py
│   ├── number_two_test_setup.py
│   └── README.md
├── 01_lcel_basics/
│   ├── step1_lcel.py
│   └── README.md
├── 02_tools_and_schemas/
│   ├── step2_structured_output.py
│   ├── structured_output_exericise.py
│   ├── step3_tool_calling.py
│   └── README.md
├── requirements.txt
├── .gitignore
└── README.md
```

## Быстрый старт (Manjaro Linux)

1. Установите необходимое, если ещё нет:

```bash
sudo pacman -S python python-pip git
```

2. Скачайте проект и создайте виртуальное окружение:

```bash
git clone https://github.com/Ramazan101/LangChain-Open-Course.git
cd LangChain-Open-Course
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Создайте в корне проекта файл `.env` с ключами. Этот файл перечислен в `.gitignore` и на GitHub не попадёт:

```ini
OPENROUTER_API_KEY=ваш_ключ_openrouter

# необязательно: трассировка в LangSmith
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=ваш_ключ_langsmith
LANGSMITH_PROJECT=langchain-open-course
```

4. Запустите проверку и любой из скриптов:

```bash
python 00_setup/test_setup.py
python 01_lcel_basics/step1_lcel.py
python 02_tools_and_schemas/step3_tool_calling.py
```

## Рекомендуемый порядок изучения

1. Модуль 00: убедиться, что связь с моделью работает.
2. Модуль 01: понять, как собираются цепочки.
3. Модуль 02, часть А: получать от модели данные по схеме.
4. Модуль 02, часть Б: давать модели инструменты.
5. Далее: RAG и агенты (модули 03 и 04).

## Как пользоваться справочниками

В каждом справочнике одна и та же структура: зачем нужен модуль, объяснение для новичка, объяснение для профи, список файлов, таблица терминов, таблица «кто что выполняет», схема потока данных, разбор кода, примеры, частые ошибки, вопросы для самопроверки и краткие выводы.

## Важное

- Секреты хранятся только в `.env`.
- Названия бесплатных моделей меняются, при ошибке «модель не найдена» сверьте название с каталогом OpenRouter.
