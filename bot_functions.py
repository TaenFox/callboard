import datetime as dt
from aiogram.types import Message
from aiogram.enums import ChatType
import uuid
import callboard
from model.card import Card
from model.chat import Chat
import re

def create_board(cards_data, external_chat_id:str) -> str:
    result = []
    for hashtag, cards in cards_data.items():
        result.append(f"{hashtag}:")
        for card in cards:
            result.append(format_card_text(card))
        result.append("")  # Пустая строка для разделения
    chat = Chat().from_dict(callboard.get_chat_by_external_id(external_chat_id))
    chat.last_published = dt.datetime.now().timestamp()
    callboard.modify_chat(chat)
    return "\n".join(result)


def format_card_text(card:dict):
    '''Функция используется для вывода текста card в сообщение отчёёт /board'''
    datetime_card = dt.datetime.fromtimestamp(card['publish_date'])
    datetime_card_formated = datetime_card.strftime("%H:%M %d.%m")
    if card['has_link']: datetime_card_formated = f"[{datetime_card_formated}]({card['link']})"
    text_preview:str = card["text"][:80] + ("..." if len(card["text"]) > 80 else "")
    return f"{datetime_card_formated} {text_preview}"


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


def can_generate_link(message: Message) -> bool:
    """
    Проверяет, можно ли создать ссылку на сообщение.
    Может вернуть либо False, либо ссылку
    """
    message_url = message.get_url()
    if message_url == None: return False
    return message_url

def set_remove_offset(message_text:str, chat_id:str, chat_name:str, bot_name:str, path_chat:str=""):
    '''Функция проверяет аргументы вызова команды изменения 
    настройки удаления объявлений, если валидные - сохраняет 
    и возвращает текст для отправки в чат'''
    chat_dict = callboard.get_chat_by_external_id(chat_id, path_chat)
    chat = Chat()
    if chat_dict != None: 
        chat.from_dict(chat_dict)
    else:
        chat.external_chat_id = chat_id
        chat.internal_chat_id = str(uuid.uuid4())
        chat.chat_name = chat_name
        callboard.add_chat(chat, path_chat)
    try:
        argument = message_text
        argument = argument.replace(f"/setremoveoffset@{bot_name}", "")
        argument = argument.replace("/setremoveoffset", "")
        if argument[0]==" ": argument=argument[1:]
        if argument[len(argument)-1]==" ": argument=argument[:len(argument)-1]
        offset = int(argument)  #TODO тут нужно пофиксить если нет чисел
        if offset <= 0: 
            return f"Укажите положительное число часов. Вы указали `{argument}`"
        chat.removing_offset = offset
        callboard.modify_chat(chat)
        return f"Установлено время удаления: новые объявления будут удаляться через `{offset}` часов"
    except Exception as e:
        print(f"Ошибка при установке времени удаления: {e}")
        return "Ошибка при установке времени удаления"

def set_publish_offset(message_text:str, chat_id:str, chat_name:str, bot_name:str, path_chat:str=""):
    '''Функция проверяет аргументы вызова команды изменения 
    настройки публикации автоматического сообщения, если валидные - сохраняет 
    и возвращает текст для отправки в чат'''
    chat_dict = callboard.get_chat_by_external_id(chat_id, path_chat)
    chat = Chat()
    if chat_dict != None: 
        chat.from_dict(chat_dict)
    else:
        chat.external_chat_id = chat_id
        chat.internal_chat_id = str(uuid.uuid4())
        chat.chat_name = chat_name
        callboard.add_chat(chat, path_chat)
    try:
        argument = message_text
        argument = argument.replace(f"/setpublishoffset@{bot_name}", "")
        argument = argument.replace("/setpublishoffset", "")
        if argument[0]==" ": argument=argument[1:]
        if argument[len(argument)-1]==" ": argument=argument[:len(argument)-1]
        offset = int(argument)  #TODO тут нужно пофиксить если нет чисел
        if offset <= 0: 
            return f"Укажите положительное число часов. Вы указали `{argument}`"
        chat.republish_offset = offset
        callboard.modify_chat(chat)
        return f"Установлено время публикации: через `{offset}` часов"
    except Exception as e:
        print(f"Ошибка при установке времени публикации: {e}")
        return "Ошибка при установке времени публикации"
    
def record_card(message:Message, bot_username:str, path_card:str="", path_chat:str = ""):
    try:
        chat_id = str(message.chat.id)
        chat_fullname = message.chat.full_name
        message_id = str(message.message_id)
        message_text = message.text
        from_user_id = str(message.from_user.id)

        chat_dict = callboard.get_chat_by_external_id(chat_id, path_chat)
        chat = Chat()
        if chat_dict != None: 
            chat.from_dict(chat_dict)
        else:
            chat.external_chat_id = chat_id
            chat.internal_chat_id = str(uuid.uuid4())
            chat.chat_name = chat_fullname
            callboard.add_chat(chat, path_chat)

        hashtags = re.findall(r"#\w+", message_text)
        card_text = create_card_text(message_text, bot_username, hashtags)
        delete_time = dt.datetime.now() + dt.timedelta(hours=chat.removing_offset)

        card = Card()
        card.card_id = str(uuid.uuid4())
        card.message_id = message_id
        card.external_user_id = from_user_id
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
        if callboard.add_card(card, path_card) == None:
            return False
        return True
    except Exception as e:
        print(f"Ошибка записи объявления: {e}")
        return False