"""
Модели и настройки SQLAlchemy для бота поддержки.
"""

from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)


# Конфигурация базы данных
DATABASE_URL = "sqlite+aiosqlite:///database.db"

# Инициализация асинхронного движка SQLAlchemy
engine = create_async_engine(DATABASE_URL)

# Создание фабрики асинхронных сессий
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    """
    Модель пользователя.
    Связывает `user_id` Telegram с `message_thread_id` и флагом блокировки.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    message_thread_id: Mapped[int] = mapped_column(Integer)
    is_blocked: Mapped[bool] = mapped_column(Boolean)


async def init_db() -> None:
    """
    Инициализирует базу данных, создавая все таблицы.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)