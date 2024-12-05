import json, os, re

class FileDataBase():
    def __init__(self, catalog:str) -> None:
        # self.catalog = f"{os.curdir}/data/{catalog}"
        self.catalog = f"{catalog}"


    def get_by_id(self, id:str)-> dict:
        '''Извлекает информацию из json-файла в указанной директории, 
        название которого соответствует маске `{id}.json`. 
        Возвращает словарь'''
        #TODO обработать ситуации, когда файл не существует
        try:
            with open(f"{self.catalog}/{id}.json", "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                return data
        except Exception as e:
            print(f"Can't read file {id}.json: {e}")
            return None

    def add_by_id(self, id:str, data:dict)-> dict:
        '''Сохраняет информацию в json-файл в указанной директории, 
        название которого соответствует маске `{id}.json`.
        В случае успеха возвращает сохранённый словарь значений'''
        try:
            json_file = open(f"{self.catalog}/{id}.json", "x", encoding="utf-8")
            json_file.write(json.dumps(data))
            json_file.close()
        except Exception as e:
            print(f"Can't create file {id}.json: {e}")
            return None
        
        try:
            savedData = self.get_by_id(id=id)
            if savedData == None: raise Exception("File does not exist")
            if data != savedData: raise Exception("Input data doesn't match with saved data")
            return savedData
        except Exception as e:
            print(f"Error creating file {id}.json: {e}")
            return None
        
    def modify_by_id(self, id:str, data:dict):
        '''Изменяет информацию в json-файл в указанной директории, 
        название которого соответствует маске `{id}.json`.
        В случае успеха возвращает сохранённый словарь значений'''
        try:
            json_file = open(f"{self.catalog}/{id}.json", "w", encoding="utf-8")
            json_file.write(json.dumps(data))
            json_file.close()
        except Exception as e:
            print(f"Can't modify file {id}.json: {e}")

        try:
            savedData = self.get_by_id(id=id)
            if savedData == None: raise Exception("File does not exist")
            if data != savedData: raise Exception("Input data doesn't match with saved data")
            return savedData
        except Exception as e:
            print(f"Error creating file {id}.json: {e}")
            return None
        
    def get_list(self):
        '''Получает список файлов в директории и их 
        содержимого как список словарей'''
        try:
            files = os.listdir(self.catalog)
            files_list:list = []
            file_name:str
            for file_name in files:
                if not re.match("[A-Za-z|\-|0-9]+(\.json)", file_name): continue
                with open(f"{self.catalog}/{file_name}", "r", encoding="utf-8") as json_file:
                    json_data = json.load(json_file)
                files_list.append(json_data)
            return files_list
        except Exception as e:
            print(f"Can't create list of files: {e}")
            return None
        
    def delete_by_id(self, id):
        '''Удаляет содержимое записи по id'''
        try:
            os.remove(f"{self.catalog}/{id}.json")
            return True
        except Exception as e:
            print(f"Can't delete file '{self.catalog}/{id}.json': {e}")
            return None