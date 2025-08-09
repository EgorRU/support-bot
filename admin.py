"""
Маршруты и обработчики сообщений админов в группе.
Пересылает ответы из темы форума пользователю, фильтруя сервисные события,
и при недоставке пишет уведомление в тему. Ставит реакцию 👍 на отправленные сообщения.
"""

from aiogram import Router, F
from aiogram.types import Message, ReactionTypeEmoji
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from setting import settings, bot
from dbrequest import get_user_id_by_message_thread_id


admin_router = Router()


@admin_router.message(
    F.chat.id == settings.GROUP_ID,
    F.chat.type.in_({"group", "supergroup"}),
    F.reply_to_message,
    ~F.forum_topic_edited,
    ~F.forum_topic_created,
    ~F.forum_topic_closed,
    ~F.forum_topic_reopened,
    ~F.pinned_message,
)
async def answer(message: Message) -> None:
    """
    Пересылает сообщение из темы форума пользователю (только текст/медиа, без сервисных событий).
    При невозможности доставки пишет уведомление в тему. Ставит реакцию 👍 в теме.
    """

    # определяем пользователя по теме
    message_thread_id = message.message_thread_id
    user_id = await get_user_id_by_message_thread_id(message_thread_id)

    # попытка отправить сообщение
    try:
        await bot.copy_message(
            chat_id=user_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
        )

    # пользователю нельзя написать
    except (TelegramBadRequest, TelegramForbiddenError):
        # используем текущую тему из сообщения без обращений к БД
        message_thread_id = message.message_thread_id

        await bot.send_message(
            chat_id=settings.GROUP_ID,
            text="[!] Пользователь заблокировал бота",
            message_thread_id=message_thread_id,
        )
        return

    # возвращаем реакцию в теме как подтверждение отправки
    await bot.set_message_reaction(
        chat_id=message.chat.id,
        message_id=message.message_id,
        reaction=[ReactionTypeEmoji(emoji="👍")],
    )