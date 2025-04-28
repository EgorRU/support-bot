from aiogram import Router, Bot, F
from aiogram.types import Message, ReactionTypeEmoji

from config import TOKEN, GROUP_ID

from dbrequest import select_users, update_user, get_user_id_from_message_thread_id

admin_router = Router()
bot = Bot(TOKEN)


@admin_router.message(F.chat.type.in_({"group", "supergroup"}))
async def answer(message: Message):
    # если первое сообщение или событие изменение темы
    if not message.reply_to_message or message.forum_topic_edited:
        return

    # отправка сообщения конкретному пользователю
    try:
        message_thread_id = message.message_thread_id
        user_id = await get_user_id_from_message_thread_id(message_thread_id)
        await bot.copy_message(
            chat_id=user_id, 
            from_chat_id=message.chat.id, 
            message_id=message.message_id,
        )
        await update_user(user_id, False)
    except:
        await update_user(user_id, True)
        message_thread_id = (await select_users())[user_id]
        await bot.send_message(
            chat_id=GROUP_ID, 
            text="[!] Пользователь заблокировал бота",
            message_thread_id=message_thread_id
        )

    # ставим реакцию, что сообщение точно отправлено
    await bot.set_message_reaction(
        chat_id=message.chat.id,
        message_id=message.message_id,
        reaction=[ReactionTypeEmoji(emoji="🔥")]
    )