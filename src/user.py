"""
Маршруты и обработчики пользовательских сообщений.
Создаёт/находит тему форума в группе по пользователю (get-or-create с защитой от гонок),
пересылает сообщения пользователя в соответствующую тему и ставит реакцию 👍 пользователю.
Название темы: "Имя Фамилия | @username" (если есть username), обрезается до 128 символов.
"""

from aiogram import Router, F
from aiogram.types import Message, ReactionTypeEmoji

from setting import settings, bot
from dbrequest import create_user, get_thread_id_by_user_id


user_router = Router()


@user_router.message(F.chat.type == "private")
async def user(message: Message) -> None:
    """
    Обрабатывает личные сообщения от пользователей.
    Приветствует при /start, создаёт тему, пересылает сообщения и ставит реакцию.
    """

    if message.text and message.text.startswith("/start"):
        await message.answer("Привет! Напиши свой вопрос, и мы с радостью тебе поможем")

    # данные пользователя
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username

    # пытаемся получить тему пользователя, если нет — безопасно создаём
    message_thread_id = await get_thread_id_by_user_id(user_id)
    if message_thread_id is None:
        # формируем ожидаемое имя темы и при расхождении можем обновить
        topic_name = f"{full_name} | @{username}" if username else full_name
        topic_name = topic_name[:128]

        response = await bot.create_forum_topic(
            chat_id=settings.GROUP_ID, name=topic_name
        )
        created = await create_user(user_id, response.message_thread_id)
        if created:
            message_thread_id = response.message_thread_id
        else:
            # запись уже появилась в БД параллельно — используем её и удаляем лишнюю тему
            message_thread_id = await get_thread_id_by_user_id(user_id)
            try:
                await bot.delete_forum_topic(
                    chat_id=settings.GROUP_ID,
                    message_thread_id=response.message_thread_id,
                )
            except Exception:
                pass

    # пересылаем сообщение пользователя в группу в его тему
    await bot.copy_message(
        chat_id=settings.GROUP_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        message_thread_id=message_thread_id,
    )
    
    # ставим реакцию пользователю, что сообщение отправлено
    await bot.set_message_reaction(
        chat_id=message.chat.id,
        message_id=message.message_id,
        reaction=[ReactionTypeEmoji(emoji="👍")],
    )