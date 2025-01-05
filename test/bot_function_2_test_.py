'''Файл содержит проблемные тесты, которые у меня не отображаются в VS Code - Павел
Запускать командой `pytest test/bot_function_2_test_.py`'''
import uuid
import datetime as dt

import sys
import os.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import pytest
from model.card import Card
from model.chat import Chat
import bot_functions as f
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
    f.callboard.add_chat(
        new_chat=Chat().from_dict(chat_data),
        path=temp_catalog_chat
    )

    result = f.set_remove_offset(
        message_text="/setremoveoffset 0",
        chat_id=chat_id,
        chat_name=chat_name,
        bot_name=bot_name,
        path_chat=temp_catalog_chat)
    assert len(result) > 0
    assert result == "Укажите положительное число часов. Вы указали `0`"

    result = f.set_remove_offset(
        message_text="/setremoveoffset 0",
        chat_id=chat_id,
        chat_name=chat_name,
        bot_name=bot_name,
        path_chat=temp_catalog_chat)
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
    f.callboard.add_chat(
        new_chat=Chat().from_dict(chat_data),
        path=temp_catalog_chat
    )

    result = f.set_publish_offset(
        message_text="/setpublishoffset 0",
        chat_id=chat_id,
        chat_name=chat_name,
        bot_name=bot_name,
        path_chat=temp_catalog_chat)
    assert len(result) > 0
    assert result == "Укажите положительное число часов. Вы указали `0`"

    result = f.set_publish_offset(
        message_text="/setpublishoffset 0",
        chat_id=chat_id,
        chat_name=chat_name,
        bot_name=bot_name,
        path_chat=temp_catalog_chat)
    assert len(result) > 0
    assert result == "Установлено время публикации: через `1` часов"

def test_create_board(temp_catalog_chat):
    '''Проверяет сообщение, генерируемуое
    функцией `bot_function.create_board'''
    chat_id = "1234567890"
    user_id = "1234567890"
    chat_data = {
        "external_chat_id": chat_id,
        "internal_chat_id": chat_id,
        "chat_name": "Test chat",
        "republish_offset": 24,
        "last_publish": dt.datetime.now().timestamp(),
        "removing_offset": 24,
        "need_to_pin": False,
        "previous_pin_id": None,
        "banned_users": []
    }
    f.callboard.add_chat(
        new_chat=Chat().from_dict(chat_data),
        path=temp_catalog_chat
    )
    card_id = str(uuid.uuid4())
    card = Card()
    card.card_id = card_id
    card.message_id = card_id
    card.external_user_id = user_id
    card.chat_id = chat_id
    card.internal_chat_id = chat_id
    card.text = "Example text for deleting user cards in callboard"
    card.hashtags = []
    card.delete_until = ""
    card.publish_date = dt.datetime.now().timestamp()
    card.has_link = False
    card.link = ""
    f.callboard.add_card(
        new_card=card,
        path=temp_catalog_card)
    cards = {"hashtag": [card.to_dict()]}
    result = f.create_board(cards, chat_id, temp_catalog_chat)
    assert len(result)>1
