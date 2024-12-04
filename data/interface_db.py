from data.file_db import FileDataBase
# import os

class CardDTO():
    path: str
    db: FileDataBase

    def __init__(self, path:str = "") -> None:
        if path == "":
            path = "./data/card"

        self.db = FileDataBase(path)

    def get_card_by_id(self, card_id:str)-> dict:
        '''Получает словарь значений, соответствующих записи с id={card_id}'''
        try:
            data = self.db.get_by_id(card_id)
            return data
        except Exception as e:
            print(f"Can't get card by id = {card_id}: {e}")
            return None

    def add_card_by_id(self, card_id:str, data:dict)-> dict:
        '''Сохраняет словарь значений, переданных в словаре data. 
        Сохраняется с id={card_id}. Возвращает результат сохранения'''
        try:
            self.db.add_by_id(card_id, data)
            data = self.db.get_by_id(card_id)
            return data
        except Exception as e:
            print(f"Can't add card by id = {card_id}: {e}")
            return None

    def modify_card_by_id(self, card_id:str, data:dict)-> dict:
        '''Заменяет словарь значений, переданных в словаре data в файле
        с id={card_id}. Возвращает результат сохранения'''
        try:
            self.db.modify_by_id(card_id, data)
            data = self.db.get_by_id(card_id)
            return data
        except Exception as e:
            print(f"Can't modify card by id = {card_id}: {e}")
            return None