from data.interface_db import CardDTO
from model.card import Card

def add_card(new_card:Card, path:str = ""):
    '''Добавить новую запись card'''
    try:
        result = CardDTO().add_card_by_id(new_card.card_id, new_card.to_dict())
        if result == None: raise Exception("Can't add card")
        return result
    except Exception as e:
        print(e)
        return None

def list_card(path:str = ""):
    '''Получить список всех записей card'''
    try:
        result = CardDTO(path).get_card_list()
        if result==None: raise Exception("No card list!")
        
        try:
            callboard_by_hashtags = {}
            for card_dict in result:
                card = Card()
                card.from_dict(card_dict)
                if len(card.hashtags)==0: 
                    card.hashtags.append("no hashtag")

                    modify_result = CardDTO(path).modify_card_by_id(card.card_id, card.to_dict())
                    if modify_result == None: raise Exception("Can't modify card record")

                for hashtag in card.hashtags:
                    if hashtag not in callboard_by_hashtags: 
                        callboard_by_hashtags[hashtag] = []
        except Exception as e:
            print(f"Can't combine hashtag list from cards: {e}")
            return None
        
        try:
            for card_dict in result:
                card = Card()
                card.from_dict(card_dict)
                for hashtag in callboard_by_hashtags:
                    if hashtag in card.hashtags:
                        callboard_by_hashtags[hashtag].append(card.to_dict())
        except Exception as e:
            print(f"Can't combine blocks of card by hashtag: {e}")
            return None
        
        return callboard_by_hashtags
        
    except Exception as e:
        print(f"Error while combine card list: {e}")
        return None

def clear(path:str = ""):
    '''Очистить устаревшие card'''