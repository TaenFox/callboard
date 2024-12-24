import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReactionTypeEmoji, BotCommand
from aiogram.filters import Command
from aiogram import F
from aiogram.enums import ChatType
import re
import asyncio
import callboard
from model.card import Card
from model.chat import Chat
import datetime as dt
import uuid

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
            board_text = create_board(cards_data)
            await message.reply(board_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Ошибка при обработке команды /board: {e}")
        await message.reply("Произошла ошибка при создании доски.")

# Обработчик команды /clearboard
@dp.message(Command("clearboard"))
async def handle_clearboard_command(message: Message):
    try:
        await clear()
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

# Хендлер для сообщений
@dp.message(F.text)
async def handle_mention(message: Message):
    bot_username = (await bot.get_me()).username

    if f"@{bot_username}" in message.text:
        chat_dict = callboard.get_chat_by_external_id(str(message.chat.id))
        chat = Chat()
        if chat_dict != None: 
            chat.from_dict(chat_dict)
        else:
            chat.external_chat_id = str(message.chat.id)
            chat.internal_chat_id = str(uuid.uuid4())
            chat.chat_name = message.chat.full_name
            callboard.add_chat(chat)

        hashtags = re.findall(r"#\w+", message.text)
        card_text = create_card_text(str(message.text), bot_username, hashtags)
        delete_time = dt.datetime.now() + dt.timedelta(hours=chat.removing_offset)

        card = Card()
        card.card_id = str(uuid.uuid4())
        card.message_id = str(message.message_id)
        card.external_user_id = str(message.from_user.id)
        card.chat_id = chat.external_chat_id
        card.internal_chat_id = chat.internal_chat_id
        card.text = card_text
        card.delete_until = delete_time.timestamp()
        card.publish_date = dt.datetime.now().timestamp()
        card.hashtags = hashtags
        link = can_generate_link(message)
        if link == False: card.has_link = False
        else:
            card.has_link = True
            card.link = link

        # Вызов функции add_card
        callboard.add_card(card)
        
        # Оставляем реакцию "✍️" (пишущая рука) на сообщение
        try:
            await bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[ReactionTypeEmoji(emoji="✍️")]  # Список реакций, поддерживаемых ботом
            )
            # if card.has_link:
            #     chat_id = message.chat.id
            #     message_id = message.message_id

            #     # Формируем ссылку для супергрупп и групп
            #     if message.chat.username:
            #         link = f"https://t.me/{message.chat.username}/{message_id}"
            #     else:
            #         link = f"https://t.me/c/{str(chat_id).lstrip('-100')}/{message_id}"

            #     await message.reply(f"Ссылка на это сообщение: {link}")
            # else:
            #     await message.reply("На это сообщение нельзя создать ссылку.")
        except Exception as e:
            print(f"Ошибка при добавлении реакции: {e}")

def can_generate_link(message: Message) -> bool:
    """
    Проверяет, можно ли создать ссылку на сообщение.
    Может вернуть либо False, либо ссылку
    """
    # Личные сообщения всегда возвращают False
    if message.chat.type == ChatType.PRIVATE:
        return False

    # Группы и супергруппы позволяют создавать ссылки на сообщения
    if message.chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}:
        if str(message.chat.id)[:4] != "-100" or message.chat.username in [None, ""]: return False
        external_chat_id = str(message.chat.id)
        if external_chat_id[:4] == "-100": external_chat_id = external_chat_id[4:]
        link = f"https://t.me/c/{external_chat_id}/{str(message.message_id)}"
        return link

    # Каналы исключаются из проверки (в задаче указано)
    if message.chat.type == ChatType.CHANNEL:
        return False

    return False

def create_card_text(original_text:str, botname:str, hashtags:list):
    '''Функция используется для формирования текста для card. Этот текст будет сохранён'''
    output = original_text
    output = output.replace("@"+botname, "")
    for hashtag in hashtags:
        output = output.replace(hashtag, "") # символ "#" включен в хештег
    while "  " in output:
        output = output.replace("  ", " ")
    if output[0]==" ": output=output[1:]
    if output[len(output)-1]==" ": output=output[:len(output)-1]
    return output

def create_board(cards_data):
    result = []
    for hashtag, cards in cards_data.items():
        result.append(f"{hashtag}:")
        for card in cards:
            result.append(format_card_text(card))
        result.append("")  # Пустая строка для разделения
    return "\n".join(result)

def format_card_text(card:dict):
    '''Функция используется для вывода текста card в сообщение отчёёт /board'''
    datetime_card = dt.datetime.fromtimestamp(card['publish_date'])
    datetime_card_formated = datetime_card.strftime("%H:%M %d.%m")
    if card['has_link']: datetime_card_formated = f"[{datetime_card_formated}]({card['link']})"
    text_preview:str = card["text"][:80] + ("..." if len(card["text"]) > 80 else "")
    return f"{datetime_card_formated} {text_preview}"

async def clear():
    callboard.clear()
    print("Очистили доску")

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
