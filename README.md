# auto_post_bot

Асинхронный сервис для автоматического сбора контента из Google Sheets и публикации по расписанию в тематические топики Telegram-супергрупп.

## Архитектура и стек

- **Python 3.12**
- **aiogram 3.x** — асинхронное взаимодействие с Telegram Bot API, отправка сообщений в треды (topics)
- **Google API Client / google-auth** — интеграция с Google Sheets API v4 по OAuth2 (Service Account)
- **APScheduler / asyncio** — планирование задач и неблокирующий цикл проверки обновлений
- **Poetry** — изоляция окружения и управление зависимостями

## Логика работы

1. `api_handler.py` авторизуется в Google API через сервисный аккаунт (`credentials.json`) и забирает сырые строки таблицы по заданному диапазону.
2. `bot_handler.py` классифицирует контент по категориям (`Projects`, `Vacancies`, `As is`), форматирует сообщения с гиперссылками и сопоставляет их с соответствующими `message_thread_id` в Telegram.
3. `scheduler.py` контролирует интервалы публикации и временные слоты отправки.
4. `main.py` выступает точкой входа, реализуя воркер с обработкой ошибок и таймаутами при отсутствии новых данных.

## Структура проекта

```text
auto_post_bot/
├── src/
│   ├── __init__.py
│   ├── api_handler.py    # Взаимодействие с Google Sheets API
│   ├── bot_handler.py    # Форматирование и отправка постов в Telegram
│   └── scheduler.py      # Планировщик очереди публикаций
├── .env.sample           # Пример переменных окружения
├── pyproject.toml        # Зависимости и конфигурация сборки
└── main.py               # Точка входа в приложение
```

## Требования

- Python 3.12+
- Poetry
- Сервисный аккаунт Google Cloud с включенным Google Sheets API
- Telegram Bot Token

## Установка и запуск

1. Клонировать репозиторий:
```bash
git clone https://github.com/Cozdig/auto_post_bot.git
cd auto_post_bot
```

2. Установить зависимости:
```bash
poetry install
```

3. Настроить конфигурацию:
Создать файл `.env` на основе примера:
```bash
cp .env.sample .env
```

Параметры окружения в `.env`:
```ini
token=YOUR_TELEGRAM_BOT_TOKEN
chat_id=YOUR_TARGET_CHAT_OR_CHANNEL_ID
google_sheets_id=YOUR_SPREADSHEET_ID
```

4. Добавить ключ Google Service Account:
Положить файл ключа `credentials.json` в корень проекта (файл должен иметь права на чтение таблицы `google_sheets_id`).

5. Запустить приложение:
```bash
poetry run python main.py
```

## Автор

- Артемий Трихалкин
- GitHub: https://github.com/Cozdig
- Telegram: @vgtfr
