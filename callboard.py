from data.interface_db import CardDTO, ChatDTO
from model.card import Card
from model.chat import Chat
from datetime import datetime as dt

def add_card(new_card:Card, path:str = ""):
    '''Добавить новую запись card'''
    try:
        result = CardDTO(path).add_card_by_id(new_card.card_id, new_card.to_dict())
        if result == None: raise Exception("Can't add card")
        return result
    except Exception as e:
        print(e)
        return None

def list_card(path:str = "", chat_id:str = "", by_hashtag:bool = True):
    '''Получить список всех записей card'''
    try:
        result_all = CardDTO(path).get_card_list()
        if result_all == None: raise Exception("No card list!")
        
        result = []
        if chat_id != "":
            for item in result_all:
                if "chat_id" in item and item["chat_id"]==chat_id:
                    result.append(item)
        else: result = result_all

        if by_hashtag==False: return result

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
    card_list = list_card(path, by_hashtag=False)
    try:
        for card_dict in card_list:
            try:
                card = Card().from_dict(card_dict)
                card_time = dt.fromtimestamp(card.delete_until)
                if card_time < dt.now(): 
                    CardDTO(path).delete_card_by_id(card.card_id)
            except Exception as e:
                print(f"Can't parse date. This card has been removed: {card_dict}")
                CardDTO(path).delete_card_by_id(card.card_id)
    except Exception as e:
        print(f"Can't complete cleaning: {e}")

def get_chat_by_external_id(external_chat_id:str, path:str = ""):
    '''Получить чат по идентификатору из телеграм'''
    try:
        known_chat_list = ChatDTO(path).get_chat_list()
        for chat_dict in known_chat_list:
            if external_chat_id == chat_dict['external_chat_id']: return chat_dict
        return None
    except Exception as e:
        print(e)
        return None
    
def get_chat_by_internal_id(internal_chat_id:str, path:str = ""):
    '''Получить чат по внутреннему идентификатору'''
    try:
        result = ChatDTO(path).get_chat_by_id(internal_chat_id)
        if result!=None: return result
        else: raise Exception("Can't find chat")
    except Exception as e:
        print(e)
        return None

def add_chat(new_chat:Chat, path:str = ""):
    '''Добавить настройки чата после предварительной проверки на отсутствие'''
    try:
        if get_chat_by_external_id(new_chat.external_chat_id) == None:
            result = ChatDTO(path).add_chat_by_id(new_chat.internal_chat_id, new_chat.to_dict())
        if result == None: raise Exception("Can't add chat")
        return result
    except Exception as e:
        print(e)
        return None