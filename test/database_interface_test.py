import sys 
import os.path 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..") 

from data.interface_db import CardDTO
import pytest
import uuid, json

@pytest.fixture
def temp_catalog_user(tmp_path):
    '''Создаёт временный каталог user для тестов.'''
    catalog = tmp_path / 'data' / 'user'
    catalog.mkdir(parents=True, exist_ok=True)
    return catalog

@pytest.fixture()
def temp_catalog_card(tmp_path):
    '''Создаёт временный каталог card для тестов.'''
    catalog = tmp_path / 'data' / 'card'
    catalog.mkdir(parents=True, exist_ok=True)
    return catalog

@pytest.fixture
def fix_card_data():
    '''Пресет данных для фидбека'''
    return  {
        "card_id": str(uuid.uuid4())
    }

def test_add_card(temp_catalog_card, fix_card_data):
    card_id = fix_card_data['card_id']
    CardDTO(temp_catalog_card).add_card_by_id(card_id, fix_card_data)

    file_path = temp_catalog_card / f"{card_id}.json"
    assert file_path.exists()

    with open(file_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
        assert saved_data == fix_card_data

def test_get_card(temp_catalog_card, fix_card_data):
    card_id = fix_card_data['card_id']
    CardDTO(temp_catalog_card).add_card_by_id(card_id, fix_card_data)
    exist_card_data = CardDTO(temp_catalog_card).get_card_by_id(card_id)
    assert exist_card_data == fix_card_data