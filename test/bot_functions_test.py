import sys 
import os.path 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..") 

from data.interface_db import CardDTO
from data.interface_db import ChatDTO
from model.card import Card
from model.chat import Chat
import bot_functions as f
import pytest, uuid
import datetime as dt
# import debugpy
# debugpy.listen(("0.0.0.0", 5678))  # Укажите порт
# print("Waiting for debugger to attach...")
# debugpy.wait_for_client()

@pytest.fixture()
def temp_catalog_card(tmp_path):
    '''Создаёт временный каталог card для тестов.'''
    catalog = tmp_path / 'data' / 'card'
    catalog.mkdir(parents=True, exist_ok=True)
    return catalog

@pytest.fixture()
def temp_catalog_chat(tmp_path):
    '''Создаёт временный каталог chat для тестов.'''
    catalog = tmp_path / 'data' / 'chat'
    catalog.mkdir(parents=True, exist_ok=True)
    return catalog

@pytest.fixture(scope="function")
def temp_chat_dict():
    '''Создаёт словарь для тестового чата'''
    data = {
        "external_chat_id": "111",
        "internal_chat_id": str(uuid.uuid4()),
        "chat_name": "Test chat",
        "republish_offset": 24,
        "last_publish": dt.datetime.now().timestamp(),
        "removing_offset": 24,
        "need_to_pin": False,
        "previous_pin_id": None,
        "banned_users": []
    }
    return data


@pytest.fixture(scope="function")
def temp_user_dict():
    '''Создаёт словарь с данными пользователя'''
    return {
        "user_id":"123"
    }

def temp_card_dict(temp_chat_dict, temp_user_dict):
    '''Создаёт словарь для тестовой карточки'''
    data =  {
        "card_id": str(uuid.uuid4()),
        "message_id": "1",
        "external_user_id": temp_user_dict["user_id"],
        "chat_id": temp_chat_dict["external_chat_id"],
        "internal_chat_id": temp_chat_dict["internal_chat_id"],
        "text": "test_message",
        "hashtags": ["test","test2"],
        "delete_until": 
            (dt.datetime.now() + dt.timedelta(hours=1)).timestamp(),
        "publish_date":dt.datetime.now().timestamp(),
        "has_link":False,
        "link":""
    }
    return data

def test_format_card_text(temp_chat_dict, temp_user_dict):
    '''Проверяет функцию форматирования текста 
    для записи в карточку объявления 
    `bot_function.format_card_text`'''
    card = Card().from_dict(temp_card_dict(temp_chat_dict, temp_user_dict))
    pub_date = card.publish_date
    reference_huge_text = ("Test" * 50)[:100]
    reference_small_text = "Test"
    datetime_card_formated = \
        dt.datetime.fromtimestamp(pub_date).strftime("%H:%M %d.%m")

    card.text = reference_huge_text
    text_preview:str = reference_huge_text[:80] + \
        ("..." if len(reference_huge_text) > 80 else "")
    reference = f"{datetime_card_formated} {text_preview}"
    result = f.format_card_text(card.to_dict())
    assert reference == result

    card.text = reference_small_text
    text_preview:str = reference_small_text[:80] + \
        ("..." if len(reference_small_text) > 80 else "")
    reference = f"{datetime_card_formated} {text_preview}"
    result = f.format_card_text(card.to_dict())
    assert reference == result

def test_create_board(temp_catalog_chat, temp_chat_dict, temp_user_dict):
    '''Проверяет сообщение, генерируемуое 
    функцией `bot_function.create_board'''
    ChatDTO(temp_catalog_chat).add_chat_by_id(temp_chat_dict["internal_chat_id"], temp_chat_dict)
    cards = {"hashtag": [temp_card_dict(temp_chat_dict, temp_user_dict)]}
    result = f.create_board(cards, temp_chat_dict["external_chat_id"], temp_catalog_chat)
    assert len(result)>1

def test_create_card_text():
    '''Проверяет текст подготовленный для записи 
    в объект карточки объявления'''
    botname = "testbot"
    hashtags = ["#test"]
    reference_text = "testetstststst"
    card_text = reference_text + " @" + botname + " " + hashtags[0]
    result = f.create_card_text(card_text, botname, hashtags)
    assert len(result) > 0
    assert result == reference_text
