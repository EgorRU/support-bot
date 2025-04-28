from aiogram import Bot, Dispatcher
import asyncio

from config import TOKEN
from models import create_db
from user import user_router
from admin import admin_router


bot = Bot(TOKEN)
dp = Dispatcher()


async def main():
    await create_db()
    dp.include_router(user_router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())