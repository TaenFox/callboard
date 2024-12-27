class Card():
    card_id:str
    message_id:str
    external_user_id:str
    chat_id:str
    internal_chat_id:str
    text:str
    hashtags:list
    delete_until:str
    publish_date:str
    has_link:bool
    link:str

    def __init__(self):
        self.card_id = ""
        self.message_id = ""
        self.external_user_id = ""
        self.chat_id = ""
        self.internal_chat_id = ""
        self.text = ""
        self.hashtags = []
        self.delete_until = ""
        self.publish_date = ""
        self.has_link = False
        self.link = ""

    def from_dict(self, data:dict):
        '''Заполняет модель card данными из словаря data'''
        #TODO добавить проверки на типы данных
        try:
            self.card_id = data['card_id']
            self.message_id = data['message_id']
            self.external_user_id = data['external_user_id']
            self.chat_id = data['chat_id']
            self.internal_chat_id = data['internal_chat_id']
            self.text = data['text']
            self.hashtags = data['hashtags']
            self.delete_until = data['delete_until']
            self.publish_date = data['publish_date']
            self.has_link = data['has_link']
            self.link = data['link']
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
                "external_user_id": self.external_user_id,
                "chat_id": self.chat_id,
                "internal_chat_id": self.internal_chat_id,
                "text": self.text,
                "hashtags": self.hashtags,
                "delete_until":self.delete_until,
                "publish_date":self.publish_date,
                "has_link":self.has_link,
                "link":self.link
            }
            return data
        except Exception as e:
            print(f"Can't construct dictionary for card id={self.card_id}: {e}")
            return None