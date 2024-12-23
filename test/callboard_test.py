from data.interface_db import CardDTO
from data.interface_db import ChatDTO
from model.card import Card
from model.chat import Chat
import callboard
import pytest
import uuid, datetime

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
            card.hashtags.append(hashtag)
            card.hashtags.append("common")
            card.delete_until = ""
            card.text = "Example text for list of cards in callboard"
            card.has_link = False
            CardDTO(temp_catalog_card).add_card_by_id(card_id, card.to_dict())

    card_id = str(uuid.uuid4())
    CardDTO(temp_catalog_card).add_card_by_id(card_id, \
                             {
                                 "card_id": card_id,
                                 "message_id": card_id,
                                 "text": "Example text for list of cards in callboard (no hashtag)",
                                 "hashtags":[],
                                 "delete_until": ""
                             })
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
    CardDTO(temp_catalog_card).add_card_by_id(card_id, \
                             {
                                 "card_id": card_id,
                                 "message_id": card_id,
                                 "chat_id": "1234",
                                 "internal_chat_id": "2345678",
                                 "text": "Example text for cleaning cards in callboard",
                                 "hashtags":[],
                                 "delete_until": past_date_until.timestamp(),
                                 "publish_date": current_date.timestamp(),
                                 "has_link": False,
                                 "link": ""
                             })
    callboard.clear(temp_catalog_card)
    result = CardDTO(temp_catalog_card).get_card_by_id(card_id)
    assert result==None

    CardDTO(temp_catalog_card).add_card_by_id(card_id, \
                             {
                                 "card_id": card_id,
                                 "message_id": card_id,
                                 "chat_id": "1234",
                                 "internal_chat_id": "2345678",
                                 "text": "Example text for cleaning cards in callboard",
                                 "hashtags":[],
                                 "delete_until": future_date_until.timestamp(),
                                 "publish_date": current_date.timestamp(),
                                 "has_link": False,
                                 "link": ""
                             })
    callboard.clear(temp_catalog_card)    
    result = CardDTO(temp_catalog_card).get_card_by_id(card_id)
    assert result!=None

def test_add_and_get_chat(temp_catalog_chat):
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
        chat.removing_offset = 24
        chat.need_to_pin = False
        chat.previous_pin_id = None
        ChatDTO(temp_catalog_chat).add_chat_by_id(chat_id, chat.to_dict())
    for reference in chat_id_list:
        result_inteenal_chat_id = callboard.get_chat_by_internal_id(reference, temp_catalog_chat)
        result_external_chat_id = callboard.get_chat_by_external_id(reference + "1234567890", temp_catalog_chat)
        assert result_inteenal_chat_id!=None
        assert result_external_chat_id!=None