import sys 
import os.path 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..") 

from data.interface_db import CardDTO
from data.interface_db import ChatDTO
from model.card import Card
from model.chat import Chat as CB_Chat
import bot_functions as f
import pytest, uuid
import datetime as dt
from aiogram.types import Message, Chat, User

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

@pytest.fixture()
def temp_data_for_card():
    '''Создаёт временный объект объявления'''
    card = Card()
    date_publish = dt.datetime.now()
    card.card_id = str(uuid.uuid4())
    card.message_id = str(uuid.uuid4())
    card.external_user_id = "1234567890"
    card.hashtags.append("common")
    card.publish_date = date_publish.timestamp()
    card.delete_until = (dt.datetime.now() + dt.timedelta(hours=1)).timestamp()
    card.text = "Test text test text"
    card.has_link = False
    return card

@pytest.fixture
def mock_message():
    """
    Создаёт фиктивное сообщение.
    """
    return Message(
        message_id=1,
        date=dt.datetime.now(),
        chat=Chat(id=-1001234567890, type="supergroup", title="Test Group"),
        from_user=User(id=12345, is_bot=False, first_name="TestUser"),
        text="/admin_command",
    )

@pytest.fixture
def mock_private_message():
    """
    Создаёт фиктивное сообщение в личных сообщениях.
    """
    return Message(
        message_id=1,
        date=dt.datetime.now(),
        chat=Chat(id=12345, type="private", username="TestUser"),
        from_user=User(id=12345, is_bot=False, first_name="TestUser"),
        text="/start",  # Укажите текст команды, которую нужно тестировать
    )

def test_format_card_text(temp_data_for_card):
    card = temp_data_for_card
    date_publish = dt.datetime.now()
    card.text = \
"В большей части случаев такие тексты подразумевают понимание клиентом проблемы и поиск решения. Значит, контент должен рассказывать о преимуществах вашего предложения и закрывать возможные возражения."
    #просто длинный текст ->
    card_dict = card.to_dict()

    result = f.format_card_text(card_dict)

    datetime_card_formated = date_publish.strftime("%H:%M %d.%m")
    text_preview:str = card.text[:80] + ("..." if len(card.text) > 80 else "")
    reference = f"{datetime_card_formated} {text_preview}"

    assert len(datetime_card_formated) >0
    assert result == reference

    card.text = "Просто короткий текст"
    card_dict = card.to_dict()

    result = f.format_card_text(card_dict)

    datetime_card_formated = date_publish.strftime("%H:%M %d.%m")
    text_preview:str = card.text[:80] + ("..." if len(card.text) > 80 else "")
    reference = f"{datetime_card_formated} {text_preview}"

    assert len(datetime_card_formated) >0
    assert result == reference

def test_create_board(temp_data_for_card):
    card:Card = temp_data_for_card
    card_dict = card.to_dict()
    cards_data = {"test": [card_dict]}
    result = f.create_board(cards_data)
    assert len(result) > 0

def test_create_card_text(temp_data_for_card):
    card:Card = temp_data_for_card
    botname = "testbot"
    hashtags = ["#test"]
    reference_text = "testetstststst"
    card_text = reference_text + " @" + botname + " " + hashtags[0]
    result = f.create_card_text(card_text, botname, hashtags)
    assert len(result) > 0
    assert result == reference_text

def test_can_generate_link(mock_message, mock_private_message):
    result = f.can_generate_link(mock_message)
    assert len(result)>0
    result = f.can_generate_link(mock_private_message)
    assert result == False

def test_set_remove_offset(temp_catalog_chat):
    chat = CB_Chat()
    chat.external_chat_id = "1234567890"
    chat.internal_chat_id = "1234567890"
    chat.chat_name = "Test chat"
    chat.republish_offset = 24
    chat.removing_offset = 24
    chat.need_to_pin = False
    chat.previous_pin_id = None
    ChatDTO(temp_catalog_chat).add_chat_by_id(chat.external_chat_id, chat.to_dict())
    chat_id = chat.external_chat_id
    chat_name = chat.chat_name
    bot_name = "testbot"

    result = f.set_remove_offset("/setremoveoffset 0", chat_id, chat_name, bot_name)
    assert len(result) > 0
    assert result == "Укажите положительное число часов. Вы указали `0`"

    result = f.set_remove_offset("/setremoveoffset 1", chat_id, chat_name, bot_name)
    assert len(result) > 0
    assert result == "Установлено время удаления: новые объявления будут удаляться через `1` часов"

def test_set_republish_offset(temp_catalog_chat):
    chat = CB_Chat()
    chat.external_chat_id = "1234567890"
    chat.internal_chat_id = "1234567890"
    chat.chat_name = "Test chat"
    chat.republish_offset = 24
    chat.removing_offset = 24
    chat.need_to_pin = False
    chat.previous_pin_id = None
    ChatDTO(temp_catalog_chat).add_chat_by_id(chat.external_chat_id, chat.to_dict())
    chat_id = chat.external_chat_id
    chat_name = chat.chat_name
    bot_name = "testbot"

    result = f.set_publish_offset("/setpublishoffset 0", chat_id, chat_name, bot_name)
    assert len(result) > 0
    assert result == "Укажите положительное число часов. Вы указали `0`"

    result = f.set_publish_offset("/setpublishoffset 1", chat_id, chat_name, bot_name)
    assert len(result) > 0
    assert result == "Установлено время публикации: через `1` часов"

def test_record_card(temp_catalog_card, temp_catalog_chat, temp_data_for_card):
    card = temp_data_for_card
    CardDTO(temp_catalog_card).add_card_by_id(card.card_id, card.to_dict())
    result = CardDTO(temp_catalog_card).get_card_list()
    assert len(result) > 0
