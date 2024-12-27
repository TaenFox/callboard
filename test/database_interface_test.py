import sys 
import os.path 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..") 
# код выше - для истории, иногда pytest подлагивает и это может помочь пофиксить
from data.interface_db import CardDTO, ChatDTO
import pytest
import uuid, json

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

@pytest.fixture
def fix_card_data():
    '''Пресет данных для card'''
    return  {
        "card_id": str(uuid.uuid4())
    }

@pytest.fixture
def fix_chat_data():
    '''Пресет данных для chat'''
    return  {
        "chat_id": str(uuid.uuid4())
    }

def test_add_card(temp_catalog_card, fix_card_data):
    card_id = fix_card_data['card_id']
    CardDTO(temp_catalog_card).add_card_by_id(card_id, fix_card_data)

    file_path = temp_catalog_card / f"{card_id}.json"
    assert file_path.exists()

    with open(file_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
        assert saved_data == fix_card_data

def test_get_card(temp_catalog_card, fix_card_data):
    card_id = fix_card_data['card_id']
    CardDTO(temp_catalog_card).add_card_by_id(card_id, fix_card_data)
    exist_card_data = CardDTO(temp_catalog_card).get_card_by_id(card_id)
    assert exist_card_data == fix_card_data

def test_delete_card(temp_catalog_card, fix_card_data):
    card_id = fix_card_data['card_id']
    CardDTO(temp_catalog_card).add_card_by_id(card_id, fix_card_data)
    result = CardDTO(temp_catalog_card).delete_card_by_id(card_id)
    assert result==True

def test_add_chat(temp_catalog_chat, fix_chat_data):
    chat_id = fix_chat_data['chat_id']
    ChatDTO(temp_catalog_chat).add_chat_by_id(chat_id, fix_chat_data)

    file_path = temp_catalog_chat / f"{chat_id}.json"
    assert file_path.exists()

    with open(file_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
        assert saved_data == fix_chat_data

def test_get_chat(temp_catalog_chat, fix_chat_data):
    chat_id = fix_chat_data['chat_id']
    ChatDTO(temp_catalog_chat).add_chat_by_id(chat_id, fix_chat_data)
    exist_chat_data = ChatDTO(temp_catalog_chat).get_chat_by_id(chat_id)
    assert exist_chat_data == fix_chat_data

def test_delete_chat(temp_catalog_chat, fix_chat_data):
    chat_id = fix_chat_data['chat_id']
    ChatDTO(temp_catalog_chat).add_chat_by_id(chat_id, fix_chat_data)
    result = ChatDTO(temp_catalog_chat).delete_chat_by_id(chat_id)
    assert result==True