class Chat():
    external_chat_id:str    #id в телеграм
    internal_chat_id:str    #id в системе
    chat_name:str
    republish_offset:int  #число часов
    last_publish:str    #timestamp
    removing_offset:int
    need_to_pin:bool
    previous_pin_id:str
    banned_users:list

    def __init__(self):
        self.external_chat_id = ""
        self.internal_chat_id = ""
        self.chat_name = ""
        self.republish_offset = 24
        self.last_publish = None
        self.removing_offset = 24
        self.need_to_pin = False
        self.previous_pin_id = None
        self.banned_users = []

    def from_dict(self, data:dict):
        '''Заполняет модель chat данными из словаря'''
        #TODO добавить проверки на типы данных
        try:
            self.external_chat_id = data['external_chat_id']
            self.internal_chat_id = data['internal_chat_id']
            self.chat_name = data['chat_name']
            self.republish_offset = data['republish_offset']
            if 'last_publish' in data: self.last_publish = data['last_publish']
            self.removing_offset = data['removing_offset']
            self.need_to_pin = data['need_to_pin']
            self.previous_pin_id = data['previous_pin_id']
            if 'banned_users' in data: self.banned_users = data['banned_users']
            else: self.banned_users = []
            return self
        except Exception as e:
            print(f"Can't use 'data' dictionary: {e}")
            return None
    
    def to_dict(self):
        '''Возвращает словарь с полями из модели chat'''
        try:
            data = {
                "external_chat_id": self.external_chat_id,
                "internal_chat_id": self.internal_chat_id,
                "chat_name": self.chat_name,
                "republish_offset": self.republish_offset,
                "last_publish": self.last_publish,
                "removing_offset": self.removing_offset,
                "need_to_pin": self.need_to_pin,
                "previous_pin_id": self.previous_pin_id,
                "banned_users": self.banned_users
            }
            return data
        except Exception as e:
            print(f"Can't construct dictionary for chat id={self.external_chat_id}: {e}")
            return None