"""
Точка входа приложения: инициализация БД и запуск бота.
"""

from aiogram import Dispatcher
import asyncio

from setting import bot
from models import init_db
from user import user_router
from admin import admin_router


async def main() -> None:
    """
    Основная функция для запуска бота.
    """
    # Создание бд
    await init_db()

    # Инициализация диспетчера
    dispatcher = Dispatcher()

    # Подключение роутеров
    dispatcher.include_router(user_router)
    dispatcher.include_router(admin_router)

    # Запуск бота
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())