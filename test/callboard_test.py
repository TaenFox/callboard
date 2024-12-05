from data.interface_db import CardDTO
from model.card import Card
import callboard
import pytest
import uuid, datetime

@pytest.fixture()
def temp_catalog_card(tmp_path):
    '''Создаёт временный каталог card для тестов.'''
    catalog = tmp_path / 'data' / 'card'
    catalog.mkdir(parents=True, exist_ok=True)
    return catalog

def test_get_callboard_by_hashtag(temp_catalog_card):
    i = 0
    while i!=4:
        i+=1
        hashtag = f"test {str(i)}"
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

def test_cleaning_cards(temp_catalog_card):
    card_id = str(uuid.uuid4())
    past_date_until = datetime.datetime.now() - datetime.timedelta(hours=1)
    future_date_until = datetime.datetime.now() + datetime.timedelta(hours=1)
    CardDTO(temp_catalog_card).add_card_by_id(card_id, \
                             {
                                 "card_id": card_id,
                                 "message_id": card_id,
                                 "chat_id": "1234",
                                 "text": "Example text for cleaning cards in callboard",
                                 "hashtags":[],
                                 "delete_until": past_date_until.timestamp()
                             })
    callboard.clear(temp_catalog_card)
    result = CardDTO(temp_catalog_card).get_card_by_id(card_id)
    assert result==None

    CardDTO(temp_catalog_card).add_card_by_id(card_id, \
                             {
                                 "card_id": card_id,
                                 "message_id": card_id,
                                 "text": "Example text for cleaning cards in callboard",
                                 "hashtags":[],
                                 "delete_until": future_date_until.timestamp()
                             })
    callboard.clear(temp_catalog_card)    
    result = CardDTO(temp_catalog_card).get_card_by_id(card_id)
    assert result!=None
