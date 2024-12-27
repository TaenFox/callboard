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
            board_text = bot_functions.create_board(cards_data)
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
    result = callboard.clear()
    print("Очистили доску")
    return result

async def is_user_admin(chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
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
            print(f"Ошибка при вызове очистке доски: {e}")
        
        # Ожидание 24 часа
        await asyncio.sleep(24 * 60 * 60)

# Запуск бота
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)
    asyncio.create_task(schedule_daily_clear())

if __name__ == "__main__":
    asyncio.run(main())
