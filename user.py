"""
Маршруты и обработчики пользовательских сообщений.
Создание тем в форуме и пересылка сообщений без символа "@" в названии темы.
"""

from aiogram import Router, F
from aiogram.types import Message, ReactionTypeEmoji
from aiogram.exceptions import TelegramBadRequest

from setting import settings, bot
from dbrequest import select_users, create_user, update_user_thread_id


user_router = Router()


@user_router.message(F.chat.type == "private")
async def user(message: Message) -> None:
    """
    Обрабатывает личные сообщения от пользователей.
    Приветствует при /start, создаёт тему, пересылает сообщения и ставит реакцию.
    """

    if message.text and message.text.startswith("/start"):
        await message.answer("Привет! Напиши свой вопрос, и мы с радостью тебе поможем")

    # Данные пользователя
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    # Текущие пользователи и их темы
    users = await select_users()

    # Если пользователя ещё нет в БД — создаём тему и сохраняем
    if user_id not in users:
        topic_name = user_name

        response = await bot.create_forum_topic(
            chat_id=settings.GROUP_ID, name=topic_name
        )

        await create_user(user_id, response.message_thread_id)
        users[user_id] = response.message_thread_id

    # ID темы для конкретного пользователя
    message_thread_id = users[user_id]

    # Пересылаем сообщение пользователя в группу в его тему
    try:
        await bot.copy_message(
            chat_id=settings.GROUP_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            reply_to_message_id=message_thread_id,
        )
    except TelegramBadRequest as e:
        # Если тема была удалена, пересоздаём и повторяем отправку
        if "message to be replied not found" in str(e):
            topic_name = message.from_user.full_name
            response = await bot.create_forum_topic(
                chat_id=settings.GROUP_ID, name=topic_name
            )
            message_thread_id = response.message_thread_id
            users[user_id] = message_thread_id
            await update_user_thread_id(user_id, message_thread_id)

            await bot.copy_message(
                chat_id=settings.GROUP_ID,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                reply_to_message_id=message_thread_id,
            )
        else:
            raise

    # Ставим реакцию пользователю, что сообщение отправлено
    await bot.set_message_reaction(
        chat_id=message.chat.id,
        message_id=message.message_id,
        reaction=[ReactionTypeEmoji(emoji="🔥")],
    )