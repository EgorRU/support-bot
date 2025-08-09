# Support Bot (Aiogram)

Телеграм-бот поддержки на базе Aiogram 3 и SQLite (async). Перенаправляет личные сообщения пользователей в ветки (темы) группы, создаёт тему автоматически при первом обращении и пересылает ответы операторов обратно пользователю.

## Возможности

- Пересылка личных сообщений в соответствующие темы форума группы
- Автоматическое создание темы при первом сообщении пользователя
- Ответы из темы в группе пересылаются пользователю в личные сообщения
- Фиксация блокировок бота пользователями
- Асинхронная БД (SQLite + SQLAlchemy 2 + aiosqlite)
- Конфигурация через `.env`

## Требования

- Python 3.10+
- Аккаунт бота Telegram (через [BotFather](https://t.me/BotFather))

## Подготовка Telegram-группы (обязательно)

1. Создайте супер-группу и включите режим «Темы» (форум).
2. Добавьте бота в группу.
3. Назначьте бота администратором с правами:
   - Управление темами (Manage Topics)
   - Отправка сообщений (Send Messages)
   - Закреплять сообщения (опционально)
4. Узнайте `GROUP_ID` группы. Можно использовать бота `@getmyid_bot` или `@RawDataBot` — ID группы будет отрицательным числом (например, `-1001234567890`).

## Установка и запуск

### Windows

#### Требования
- Python 3.10+
- Git

#### Шаги

1. Клонируйте репозиторий и перейдите в папку проекта:
   ```powershell
   git clone https://github.com/EgorRU/support-bot.git
   cd support-bot
   ```
2. Создайте и активируйте виртуальное окружение:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Установите зависимости:
   ```powershell
   python -m pip install -r requirements.txt
   ```
4. Создайте файл окружения и заполните значения:
   ```powershell
   copy env_example.txt .env
   ```
   Откройте `.env` и укажите параметры:
   ```env
   BOT_TOKEN=ВАШ_ТОКЕН_БОТА
   GROUP_ID=-1001234567890
   ```
   Важно: перед ID группы обязательно должен быть префикс -100.
5. Запустите бота:
   ```powershell
   python main.py
   ```

### Linux/macOS

1. Клонируйте репозиторий и перейдите в папку проекта:
   ```bash
   git clone https://github.com/EgorRU/support-bot.git
   cd support-bot
   ```
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Установите зависимости:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
4. Создайте файл окружения и заполните значения:
   ```bash
   cp env_example.txt .env
   ```
   Отредактируйте `.env`:
   ```env
   BOT_TOKEN=ВАШ_ТОКЕН_БОТА
   GROUP_ID=-1001234567890
   ```
   Важно: перед ID группы обязательно должен быть префикс -100.
5. Запустите бота:
   ```bash
   python3 main.py
   ```

### Альтернативные способы запуска

**Через Makefile:**
```bash
make run
```

**Docker Compose**:
```bash
docker-compose up -d
```

Docker-сборка использует `requirements.txt` и запускает `python main.py`. База данных SQLite создаётся в контейнере (`database.db`).

## Структура проекта

```
support-bot/
├── main.py             # Точка входа
├── user.py             # Обработчики для пользователей
├── admin.py            # Обработчики сообщений из группы
├── dbrequest.py        # Доступ к БД
├── models.py           # ORM-модели и инициализация БД
├── setting.py          # Настройки и конфигурация (.env)
├── requirements.txt    # Зависимости Python
├── pyproject.toml      # Конфигурация проекта/инструментов
├── README.md           # Документация
├── LICENSE             # Лицензия MIT
├── Makefile            # Команды разработки
├── Dockerfile          # Контейнеризация
├── docker-compose.yml  # Docker Compose
├── .env                # Конфигурация (создать вручную)
├── .editorconfig       # Настройки редактора
├── .gitattributes      # Настройки Git
├── .gitignore          # Игнорируемые файлы
└── .dockerignore       # Игнорируемые Docker-файлы
```

## Переменные окружения (.env)

```env
BOT_TOKEN=ваш_токен_бота
GROUP_ID=-100xxxxxxxxxx
```

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для получения дополнительной информации.
