"""
Маршруты и обработчики сообщений админов в группе.
Пересылает ответы из темы форума пользователю и обрабатывает блокировки.
"""

from aiogram import Router, F
from aiogram.types import Message, ReactionTypeEmoji
from aiogram.exceptions import TelegramBadRequest

from setting import settings, bot
from dbrequest import (
    select_users,
    update_user,
    get_user_id_from_message_thread_id,
)


admin_router = Router()


@admin_router.message(F.chat.type.in_({"group", "supergroup"}))
async def answer(message: Message) -> None:
    """
    Пересылает сообщение из темы форума пользователю.
    При блокировке бота пользователем помечает это и публикует уведомление.
    """

    # Игнорируем системные сообщения:
    # 1) первое сообщение в теме (нет reply_to_message)
    # 2) события редактирования темы (forum_topic_edited)
    if not message.reply_to_message or message.forum_topic_edited:
        return

    try:
        # Идентификатор темы, из которой пришло сообщение
        message_thread_id = message.message_thread_id

        # Находим пользователя, закреплённого за этой темой
        user_id = await get_user_id_from_message_thread_id(message_thread_id)

        # Пересылаем сообщение из группы пользователю в личные сообщения
        await bot.copy_message(
            chat_id=user_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
        )

        # Пользователь не блокирует бота — отражаем это в БД
        await update_user(user_id, False)
    # Такие ошибки может выбросить Telegram, когда отправка невозможна.
    # Типичные причины:
    #  - пользователь заблокировал бота;
    #  - пользователь удалил диалог/аккаунт;
    #  - в БД остался неверный user_id (устаревшая привязка к теме).
    # В этих случаях помечаем пользователя как недоступного и пишем уведомление в тему.
    except TelegramBadRequest:
        await update_user(user_id, True)
        message_thread_id = (await select_users())[user_id]
        await bot.send_message(
            chat_id=settings.GROUP_ID,
            text="[!] Пользователь заблокировал бота",
            message_thread_id=message_thread_id,
        )
    except Exception:
        pass

    # Возвращаем реакцию в теме как подтверждение отправки
    await bot.set_message_reaction(
        chat_id=message.chat.id,
        message_id=message.message_id,
        reaction=[ReactionTypeEmoji(emoji="🔥")],
    )