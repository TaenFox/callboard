import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReactionTypeEmoji, BotCommand
from aiogram.filters import Command
from aiogram import F
import asyncio
import callboard
import bot_functions

# Получение токена бота из переменной окружения
TOKEN = os.environ.get("TOKEN_BOT_CALLBOARD")

if not TOKEN:
    raise ValueError("Токен бота не найден. Убедитесь, что переменная окружения TOKEN_BOT_CALLBOARD установлена.")

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /board
@dp.message(Command("board"))
async def handle_board_command(message: Message):
    try:
        cards_data = callboard.list_card(chat_id=str(message.chat.id))
        if len(cards_data)==0: await message.reply("Нет актуальных объявлений")
        else:
            board_text = bot_functions.create_board(cards_data, str(message.chat.id))
            await message.reply(board_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Ошибка при обработке команды /board: {e}")
        await message.reply("Произошла ошибка при создании доски.")

# Обработчик команды /clearboard
@dp.message(Command("clearboard"))
async def handle_clearboard_command(message: Message):
    try:
        result = await clear()
        if result == False: raise Exception()
        try:
            await bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[ReactionTypeEmoji(emoji="👌")]
            )
        except Exception as e:
            print(f"Ошибка при добавлении реакции: {e}")
    except Exception as e:
        print(f"Ошибка очистки доски: {e}")

@dp.message(Command("setremoveoffset"))
async def handle_setremoveoffset_command(message: Message):
    '''Сохраняет настройку времени, которая сохраняется в карточки для удаления'''
    if not await is_user_admin(message.chat.id, message.from_user.id):
        await message.reply("Действие доступно только администратору")
        return
    bot_name = (await bot.get_me()).username
    answer = bot_functions.set_remove_offset(message.text,
                                             str(message.chat.id),
                                             message.chat.full_name,
                                             bot_name)
    await message.reply(answer)

@dp.message(Command("setpublishoffset"))
async def handle_setpublishoffset_command(message: Message):
    '''Сохраняет настройку времени через сколько нужно запостить новое сообщение в канал и почистить доску'''
    if not await is_user_admin(message.chat.id, message.from_user.id):
        await message.reply("Действие доступно только администратору")
        return
    bot_name = (await bot.get_me()).username
    answer = bot_functions.set_publish_offset(message.text,
                                             str(message.chat.id),
                                             message.chat.full_name,
                                             bot_name)
    await message.reply(answer)

@dp.message(Command("ban"))
async def handle_ban_command(message: Message):
    '''Ищет упоминание пользователя в команде, 
    помещает его в чёрный список и 
    удаляет его объявления в этом чате'''
    if not await is_user_admin(message.chat.id, message.from_user.id):
        await message.reply("Действие доступно только администратору")
        return
    if message.reply_to_message == None:
        await message.reply("Ответьте командой на сообщение пользователя, которого хотите забанить")
        return
    ban_user_id= str(message.reply_to_message.from_user.id)
    reply_text = bot_functions.ban_user(ban_user_id, str(message.chat.id), message.chat.full_name)
    await message.reply(reply_text)

# Хендлер для сообщений
@dp.message(F.text)
async def handle_mention(message: Message):
    bot_username = (await bot.get_me()).username

    if f"@{bot_username}" in message.text:
        result = bot_functions.record_card(message, bot_username)
        
        try:
            if result == True:
                await bot.set_message_reaction(
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    reaction=[ReactionTypeEmoji(emoji="✍️")]
                )
            else:
                await bot.set_message_reaction(
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    reaction=[ReactionTypeEmoji(emoji="🤷")]
                )
        except Exception as e:
            print(f"Ошибка при добавлении реакции: {e}")


async def clear():
    callboard.clear()
    chats_to_republic = callboard.republic_chat_list()
    for chat_dict in chats_to_republic:
        text_message = bot_functions.create_board(
                callboard.list_card(chat_id=chat_dict["external_chat_id"]),
                chat_dict["external_chat_id"])
        if text_message != "": 
            sent_message = await bot.send_message(
                chat_id=chat_dict["external_chat_id"], 
                text=text_message,
                parse_mode="Markdown")
            await bot.pin_chat_message(chat_id=chat_dict["external_chat_id"], message_id=sent_message.message_id)
    #print("Очистили доску")

async def is_user_admin(chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        chat = await bot.get_chat(chat_id)
        return member.status in ["administrator", "creator"] \
            or chat.type == "private"
    except Exception as e:
        print(f"Ошибка при определении статуса пользователя: {e}")
        return False

async def schedule_daily_clear():
    """
    Планировщик, вызывающий функцию clear раз в сутки.
    """
    while True:
        try:
            await clear()  # Вызов функции clear
        except Exception as e:
            print(f"Ошибка при републикации: {e}")
        
        # Ожидание 5 минут
        await asyncio.sleep(360)

# Запуск бота
async def main():
    print("Бот запущен!")
    asyncio.create_task(schedule_daily_clear())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
