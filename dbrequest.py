"""
Функции доступа к базе данных для работы с пользователями.
Содержит декоратор подключения к сессии и CRUD-операции.
"""

from typing import Any, Awaitable, Callable, Dict, Optional

from models import async_session
from models import User
from sqlalchemy import select


def connection(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    """
    Оборачивает функцию в контекст асинхронной сессии SQLAlchemy.
    """

    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper


@connection
async def select_users(session) -> Dict[int, int]:
    """
    Возвращает словарь user_id -> message_thread_id для всех пользователей.
    """
    result = await session.execute(select(User.user_id, User.message_thread_id))
    users = result.all()
    return {user.user_id: user.message_thread_id for user in users}


@connection
async def create_user(session, user_id: int, message_thread_id: int) -> None:
    """
    Создаёт нового пользователя с указанной темой и статусом не заблокирован.
    """
    new_user = User(user_id=user_id, message_thread_id=message_thread_id, is_blocked=False)
    session.add(new_user)
    await session.commit()


@connection
async def get_user_id_from_message_thread_id(session, message_thread_id: int) -> Optional[int]:
    """
    Возвращает user_id по идентификатору темы сообщения.
    """
    result = await session.execute(
        select(User.user_id).where(User.message_thread_id == message_thread_id)
    )
    user_id = result.scalars().first()
    return user_id


@connection
async def update_user(session, user_id: int, is_blocked: bool) -> None:
    """
    Обновляет флаг блокировки пользователя.
    """
    result = await session.execute(select(User).where(User.user_id == user_id))
    user = result.scalars().first()

    if user:
        user.is_blocked = is_blocked
        await session.commit()


@connection
async def update_user_thread_id(session, user_id: int, message_thread_id: int) -> None:
    """
    Обновляет идентификатор темы (message_thread_id) для пользователя.
    """
    result = await session.execute(select(User).where(User.user_id == user_id))
    user = result.scalars().first()

    if user:
        user.message_thread_id = message_thread_id
        await session.commit()