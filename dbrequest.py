from models import async_session
from models import User
from sqlalchemy import select


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper


@connection
async def select_users(session):
    result = await session.execute(select(User.user_id, User.message_thread_id))
    users = result.all()
    return {user.user_id: user.message_thread_id for user in users}


@connection
async def create_user(session, user_id, message_thread_id):
    new_user = User(user_id=user_id, message_thread_id=message_thread_id, is_blocked=False)
    session.add(new_user)
    await session.commit()


@connection
async def get_user_id_from_message_thread_id(session, message_thread_id):
    result = await session.execute(select(User.user_id).where(User.message_thread_id == message_thread_id))
    user_id = result.scalars().first()
    return user_id


@connection
async def update_user(session, user_id, is_blocked):
    result = await session.execute(select(User).where(User.user_id == user_id))
    user = result.scalars().first()

    if user:
        user.is_blocked = is_blocked
        await session.commit()