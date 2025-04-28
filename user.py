from aiogram import Router, Bot, F
from aiogram.types import Message, ReactionTypeEmoji

from config import TOKEN, GROUP_ID

from dbrequest import select_users, create_user


user_router = Router()
bot = Bot(TOKEN)

@user_router.message(F.chat.type == 'private')
async def user(message: Message):
    if message.text:
        if message.text.startswith("/start"):
            await message.answer("Привет! Напиши свой вопрос, и мы с радостью тебе поможем")
            
    # данные пользователя
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    user_name = message.from_user.username
    
    # получение пользователей
    users = await select_users()

    # если пользователя нет
    if user_id not in users:
        
        # создаём ветку
        response = await bot.create_forum_topic(
            chat_id=GROUP_ID,
            name=f"{full_name}  {"- @"+user_name if user_name else ""}"
        )
        
        # создаём пользователя
        await create_user(user_id, response.message_thread_id)

        # добавляем его в локальную бд
        users[user_id] = response.message_thread_id

    # извлекаем id сообщения по конкретному пользователю
    message_thread_id = users[user_id]

    # пересылаем сообщение
    await bot.copy_message(
        chat_id=GROUP_ID, 
        from_chat_id=message.chat.id, 
        message_id=message.message_id, 
        reply_to_message_id=message_thread_id
    )

    # ставим реакцию, что сообщение отправлено
    await bot.set_message_reaction(
        chat_id=message.chat.id,
        message_id=message.message_id,
        reaction=[ReactionTypeEmoji(emoji="🔥")]
    )