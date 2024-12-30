'''Файл содержит проблемные тесты, которые у меня не отображаются в VS Code - Павел
Запускать командой `pytest test/bot_function_2_test_.py`'''
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

def test_set_remove_offset(temp_catalog_chat):
    chat_data = {
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
    chat_id = chat_data["external_chat_id"]
    chat_name = chat_data["chat_name"]
    bot_name = "testbot"
    ChatDTO(temp_catalog_chat).add_chat_by_id(chat_data["internal_chat_id"], chat_data)

    result = f.set_remove_offset("/setremoveoffset 0", chat_id, chat_name, bot_name, temp_catalog_chat)
    assert len(result) > 0
    assert result == "Укажите положительное число часов. Вы указали `0`"

    result = f.set_remove_offset("/setremoveoffset 1", chat_id, chat_name, bot_name, temp_catalog_chat)
    assert len(result) > 0
    assert result == "Установлено время удаления: новые объявления будут удаляться через `1` часов"

def test_set_republish_offset(temp_catalog_chat):
    chat_data = {
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
    chat_id = chat_data["external_chat_id"]
    chat_name = chat_data["chat_name"]
    bot_name = "testbot"
    ChatDTO(temp_catalog_chat).add_chat_by_id(chat_data["internal_chat_id"], chat_data)

    result = f.set_publish_offset("/setpublishoffset 0", chat_id, chat_name, bot_name, temp_catalog_chat)
    assert len(result) > 0
    assert result == "Укажите положительное число часов. Вы указали `0`"

    result = f.set_publish_offset("/setpublishoffset 1", chat_id, chat_name, bot_name, temp_catalog_chat)
    assert len(result) > 0
    assert result == "Установлено время публикации: через `1` часов"
