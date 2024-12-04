class Card():
    card_id:str
    message_id:str
    text:str
    hashtags:list

    def __init__(self):
        self.card_id = ""
        self.message_id = ""
        self.text = ""
        self.hashtags = []

    def from_dict(self, data:dict):
        '''Заполняет модель card данными из словаря data'''
        #TODO добавить проверки на типы данных
        try:
            self.card_id = data['card_id']
            self.message_id = data['message_id']
            self.text = data['text']
            self.hashtags = data['hashtags']
            return self
        except Exception as e:
            print(f"Can't use 'data' dictionary: {e}")
            return None
        
    def to_dict(self):
        '''Возвращает словарь с полями из модели card'''
        try:
            data = {
                "card_id": self.card_id,
                "message_id": self.message_id,
                "text": self.text,
                "hashtags": self.hashtags
            }
            return data
        except Exception as e:
            print(f"Can't construct dictionary for card id={self.card_id}: {e}")
            return None