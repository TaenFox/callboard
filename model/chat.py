class Chat():
    external_chat_id:str    #id в телеграм
    internal_chat_id:str    #id в системе
    chat_name:str
    republish_offset:int  #число часов
    removing_offset:int
    need_to_pin:bool
    previous_pin_id:str

    def __init__(self):
        self.external_chat_id = ""
        self.internal_chat_id = ""
        self.chat_name = ""
        self.republish_offset = 24
        self.removing_offset = 24
        self.need_to_pin = False
        self.previous_pin_id = None

    def from_dict(self, data:dict):
        '''Заполняет модель chat данными из словаря'''
        #TODO добавить проверки на типы данных
        try:
            self.external_chat_id = data['external_chat_id']
            self.internal_chat_id = data['internal_chat_id']
            self.chat_name = data['chat_name']
            self.republish_offset = data['republish_offset']
            self.removing_offset = data['removing_offset']
            self.need_to_pin = data['need_to_pin']
            self.previous_pin_id = data['previous_pin_id']
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
                "removing_offset": self.removing_offset,
                "need_to_pin": self.need_to_pin,
                "previous_pin_id": self.previous_pin_id
            }
            return data
        except Exception as e:
            print(f"Can't construct dictionary for chat id={self.external_chat_id}: {e}")
            return None