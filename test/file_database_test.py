from data.file_db import FileDataBase
import pytest
import json

@pytest.fixture
def temp_catalog(tmp_path):
    '''Создаёт временный каталог для тестов.'''
    catalog = tmp_path / 'test_data'
    catalog.mkdir(parents=True, exist_ok=True)
    return catalog

@pytest.fixture
def file_database(temp_catalog):
    '''Создаёт экземпляр класса FileDataBase, 
    указывая временный каталог.'''
    return FileDataBase(catalog=str(temp_catalog))

def test_add_by_id(file_database, temp_catalog):
    '''Тестирует создание нового файла и запись данных.'''
    data = {'name': 'John', 'age': 30}
    file_database.add_by_id('user1', data)
    
    file_path = temp_catalog / 'user1.json'
    assert file_path.exists()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
        assert saved_data == data

def test_get_by_id(file_database, temp_catalog):
    '''Тестирует извлечение данных из существующего файла.'''
    data = {'name': 'John', 'age': 30}
    
    file_path = temp_catalog / 'user1.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    
    retrieved_data = file_database.get_by_id('user1')
    assert retrieved_data == data

def test_modify_by_id(file_database, temp_catalog):
    '''Тестирует изменение данных в существующем файле.'''
    data = {'name': 'John', 'age': 30}
    modified_data = {'name': 'John', 'age': 35}
    
    file_path = temp_catalog / 'user1.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    
    file_database.modify_by_id('user1', modified_data)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
        assert saved_data == modified_data

def test_get_by_id_file_not_exists(file_database):
    '''Тестирует обработку случая, когда файл не существует.'''
    result = file_database.get_by_id('nonexistent')
    assert result is None

def test_get_list_of_json_files(file_database):
    '''Тестирует получение списка созданных файлов'''
    test_data = [
        {"number": 1, "colour": "red"},
        {"number": 2, "colour": "green"},
        {"number": 3, "colour": "blue"},
    ]
    for simple_data in test_data:
        file_database.add_by_id(simple_data["number"], simple_data)
    
    result_list = file_database.get_list()
    assert test_data == result_list

def test_delete_file(file_database):
    '''Тестирует удаление файла'''
    data = {'name': 'John', 'age': 30}
    id = 123
    file_database.add_by_id(id, data)

    result = file_database.delete_by_id(id)
    assert result == True