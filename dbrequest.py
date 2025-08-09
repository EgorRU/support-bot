"""
Функции доступа к базе данных для работы с пользователями.
Содержит декоратор подключения к сессии и CRUD-операции.
"""

from typing import Any, Awaitable, Callable, Optional

from models import async_session
from models import User
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


def connection(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    """
    Оборачивает функцию в контекст асинхронной сессии SQLAlchemy.
    """

    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper


@connection
async def create_user(session, user_id: int, message_thread_id: int) -> bool:
    """
    Создаёт нового пользователя с указанной темой.
    Возвращает True, если запись создана, False — если уже существовала.
    """
    new_user = User(user_id=user_id, message_thread_id=message_thread_id)
    session.add(new_user)
    try:
        await session.commit()
        return True
    except IntegrityError:
        await session.rollback()
        return False


@connection
async def get_user_id_by_message_thread_id(session, message_thread_id: int) -> Optional[int]:
    """
    Возвращает user_id по иmessage_thread_id.
    """
    result = await session.execute(
        select(User.user_id).where(User.message_thread_id == message_thread_id)
    )
    user_id = result.scalars().first()
    return user_id


@connection
async def get_thread_id_by_user_id(session, user_id: int) -> Optional[int]:
    """
    Возвращает message_thread_id по user_id.
    """
    result = await session.execute(
        select(User.message_thread_id).where(User.user_id == user_id)
    )
    thread_id = result.scalars().first()
    return thread_id