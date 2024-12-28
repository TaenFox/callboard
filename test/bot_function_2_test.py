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
import callboard

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
    card.chat_id = "1234567890"
    card.message_id = str(uuid.uuid4())
    card.external_user_id = "1234567890"
    card.hashtags.append("common")
    card.publish_date = date_publish.timestamp()
    card.delete_until = (dt.datetime.now() + dt.timedelta(hours=1)).timestamp()
    card.text = "Test text test text"
    card.has_link = False
    return card

def test_create_board(temp_data_for_card, temp_catalog_card, temp_catalog_chat):
    card:Card = temp_data_for_card
    CardDTO(temp_catalog_card).add_card_by_id(card.card_id, card.to_dict())
    ChatDTO(temp_catalog_chat).add_chat_by_id(card.chat_id, {"external_chat_id": card.chat_id, "internal_chat_id": card.chat_id, "chat_name": card.chat_id})
    chat = ChatDTO(temp_catalog_chat).get_chat_by_id(card.chat_id)
    assert "last_publish" not in chat
    card_dict = card.to_dict()
    cards_data = {"test": [card_dict]}
    result = f.create_board(cards_data, card.chat_id)
    assert len(result) > 0
    chat["last_publish"] = dt.datetime.now().timestamp()
    ChatDTO(temp_catalog_chat).modify_chat_by_id(card.chat_id, chat)
    chat = ChatDTO(temp_catalog_chat).get_chat_by_id(card.chat_id)
    assert "last_publish" in chat