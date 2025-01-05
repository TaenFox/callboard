import sys 
import os.path 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..") 

from model.card import Card
from model.chat import Chat
import callboard
import pytest
import uuid, datetime
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

def test_get_callboard_by_hashtag(temp_catalog_card):
    '''Тест проверяет функцию получения 
    списка карточек по хэштегу: 
    - результат должен быть не пустым'''
    i = 0
    hashtag_list = []
    while i!=4:
        i+=1
        hashtag = f"test {str(i)}"
        hashtag_list.append(hashtag)
        j=i
        while j!=4:
            j+=1
            card_id = str(uuid.uuid4())
            card = Card()
            card.card_id = card_id
            card.message_id = card_id
            card.external_user_id = "1234567890"
            card.hashtags.append(hashtag)
            card.hashtags.append("common")
            card.delete_until = ""
            card.text = "Example text for list of cards in callboard"
            card.has_link = False
            callboard.add_card(
                new_card=card,
                path=temp_catalog_card)

    card_id = str(uuid.uuid4())
    card.card_id = card_id
    card.message_id = card_id
    card.external_user_id = "1234567890"
    while len(card.hashtags)!=0:
        card.hashtags.pop()
    card.delete_until = ""
    card.text = "Example text for list of cards in callboard"
    card.has_link = False
    callboard.add_card(
        new_card=card,
        path = temp_catalog_card)
    result = callboard.list_card(temp_catalog_card)
    print(result)
    assert result != []
    assert len(result) == 5
    for reference in hashtag_list[:3]:  #4й хэштег не учитывается, так как по нему нет карточек
        assert reference in result

def test_cleaning_cards(temp_catalog_card):
    card_id = str(uuid.uuid4())
    past_date_until = datetime.datetime.now() - datetime.timedelta(hours=1)
    future_date_until = datetime.datetime.now() + datetime.timedelta(hours=1)
    current_date = datetime.datetime.now()
    card = Card()
    card.card_id = card_id
    card.message_id = card_id
    card.external_user_id = "12345"
    card.chat_id =  "1234"
    card.internal_chat_id = "2345678"
    card.text = "Example text for cleaning cards in callboard"
    card.delete_until = past_date_until.timestamp()
    card.publish_date = current_date.timestamp()
    callboard.add_card(
        new_card=card,
        path=temp_catalog_card)
    callboard.clear(temp_catalog_card)
    result = callboard.get_card_by_id(card_id=card_id, path=temp_catalog_card)
    assert result==None

    callboard.add_card(
        new_card=card,
        path=temp_catalog_card)  
    result = callboard.get_card_by_id(card_id=card_id, path=temp_catalog_card)
    assert result!=None

def test_add_modify_and_get_chat(temp_catalog_chat):
    '''Тест проверяет функцию добавления и получения 
    списка чатов: 
    - добавляет 4 чата
    - проверяет их наличие по внутреннему и внешнему идентификатору
    - результат должен быть не пустым'''
    i = 0
    chat_id_list = []
    while i!=4:
        i+=1
        chat_id = str(uuid.uuid4())
        chat_id_list.append(chat_id)
        chat = Chat()
        chat.external_chat_id = chat_id + "1234567890"
        chat.internal_chat_id = chat_id
        chat.chat_name = f"Chat {str(i)}"
        chat.republish_offset = 24
        chat.last_publish = datetime.datetime.now().timestamp()
        chat.removing_offset = 24
        chat.need_to_pin = False
        chat.previous_pin_id = None
        callboard.add_chat(
            new_chat = chat,
            path=temp_catalog_chat)
    for reference in chat_id_list:
        result_inteenal_chat_id = callboard.get_chat_by_internal_id(reference, temp_catalog_chat)
        result_external_chat_id = callboard.get_chat_by_external_id(reference + "1234567890", temp_catalog_chat)
        assert result_inteenal_chat_id!=None
        assert result_external_chat_id!=None
    
    modified_chat_id = chat_id_list[0]
    chat_data = callboard.get_chat_by_internal_id(modified_chat_id, temp_catalog_chat)
    modified_chat_data = chat_data.copy()
    modified_chat_data['removing_offset'] = 0
    callboard.modify_chat(
        chat=Chat().from_dict(modified_chat_data), 
        path=temp_catalog_chat)
    result_chat_data = callboard.get_chat_by_internal_id(
        internal_chat_id=modified_chat_id, 
        path=temp_catalog_chat)
    assert result_chat_data != None
    assert chat_data != result_chat_data

def test_delete_user_cards(temp_catalog_card, temp_catalog_chat):
    '''Тест проверяет функцию удаления всех карточек 
    пользователя из чата: 
    - добавляет 4 карточки
    - удаляет 2 карточки
    - проверяет наличие оставшихся карточек'''
    i = 0
    user_id = "1234567890"
    chat_id = "1234567890"
    while i!=4:
        i+=1
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
        card.publish_date = datetime.datetime.now().timestamp()
        card.has_link = False
        card.link = ""
        callboard.add_card(
            new_card=card,
            path=temp_catalog_card)
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
    callboard.add_chat(
        new_chat=Chat().from_dict(chat_data),
        path=temp_catalog_chat)
    result = callboard.list_card(
        path=temp_catalog_card, 
        internal_chat_id=chat_id, 
        by_hashtag=False)
    assert result != []
    callboard.delete_user_card(
        user_id=user_id, 
        external_chat_id=chat_id, 
        card_path=temp_catalog_card, 
        path_chat=temp_catalog_chat)
    result = callboard.list_card(
        path=temp_catalog_card, 
        internal_chat_id=chat_id, 
        by_hashtag=False)
    assert result == []

def test_ban_user(temp_catalog_card, temp_catalog_chat):
    '''Тесто проверяет функциональность бана пользователя'''
    i = 0
    user_id = "1234567890"
    chat_id = "1234567890"
    while i!=4:
        i+=1
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
        card.publish_date = datetime.datetime.now().timestamp()
        card.has_link = False
        card.link = ""
        callboard.add_card(
            new_card=card,
            path=temp_catalog_card)
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
    callboard.add_chat(
        new_chat=Chat().from_dict(chat_data),
        path=temp_catalog_chat)
    result = callboard.list_card(
        temp_catalog_card, 
        internal_chat_id=chat_id, 
        by_hashtag=False)
    assert result != []
    print(callboard.ban_user(
        ban_user_id=user_id, 
        chat_id=chat_id, 
        path_chat=temp_catalog_chat, 
        path_card=temp_catalog_card))
    result = callboard.list_card(
        path=temp_catalog_card, 
        internal_chat_id=chat_id, 
        by_hashtag=False)
    assert result == []
    chat_data = callboard.get_chat_by_external_id(
        external_chat_id=chat_id, 
        path=temp_catalog_chat)
    assert user_id in chat_data["banned_users"]
    callboard.unban_user(
        external_user_id=user_id, 
        chat_id=chat_id, 
        path_chat=temp_catalog_chat)
    chat_data = callboard.get_chat_by_external_id(chat_id, temp_catalog_chat)
    assert user_id not in chat_data["banned_users"]
    