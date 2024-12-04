class Call():
    call_id:str

    def from_dict(self, data:dict):
        '''Заполняет модель call данными из словаря data'''
        try:
            self.card_id = data['card_id']
            return self
        except Exception as e:
            print(f"Can't use 'data' dictionary: {e}")
            return None
        
    def to_dict(self):
        '''Возвращает словарь с полями из модели call'''
        try:
            data = {
                "call_id": self.call_id
            }
            return data
        except Exception as e:
            print(f"Can't construct dictionary for call id={self.call_id}: {e}")
            return None