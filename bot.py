import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReactionTypeEmoji, BotCommand
from aiogram.filters import Command
from aiogram import F
import re
import asyncio
import callboard
from model.card import Card
import datetime as dt
import uuid

# Получение токена бота из переменной окружения
TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Токен бота не найден. Убедитесь, что переменная окружения BOT_TOKEN установлена.")

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хендлер для сообщений
@dp.message(F.text)
async def handle_mention(message: Message):
    bot_username = (await bot.get_me()).username
    if f"@{bot_username}" in message.text:
        # Извлечение хэштегов
        hashtags = re.findall(r"#\w+", message.text)
        delete_time = dt.datetime.now() + dt.timedelta(days=1)
        card = Card()
        card.card_id = str(uuid.uuid4())
        card.message_id = str(message.message_id)
        card.chat_id = str(message.chat.id)
        card.text = str(message.text)
        card.delete_until = delete_time.timestamp()
        card.hashtags = hashtags

        # Вызов функции add_card
        callboard.add_card(card)
        
        # Оставляем реакцию "✍️" (пишущая рука) на сообщение
        try:
            await bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[ReactionTypeEmoji(emoji="✍️")]  # Список реакций, поддерживаемых ботом
            )
        except Exception as e:
            print(f"Ошибка при добавлении реакции: {e}")

# Запуск бота
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
