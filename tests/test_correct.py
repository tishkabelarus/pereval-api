import pytest
from app import create_app
import json

def test_complete_validation():
    """Тест с полными корректными данными"""
    app = create_app()
    
    with app.test_client() as client:
        # Данные которые ДОЛЖНЫ пройти валидацию
        correct_data = {
            'beautyTitle': 'пер. ',           # обязательное
            'title': 'Корректный тест',       # обязательное
            'other_titles': 'Другие названия',
            'connect': 'что-то соединяет',
            'user': {                         # обязательное
                'email': 'correct@test.com',  # обязательное
                'phone': '79001234567',
                'fam': 'Корректнов',          # обязательное  
                'name': 'Тест',               # обязательное
                'otc': 'Тестович'
            },
            'coords': {                       # обязательное
                'latitude': '45.1234',
                'longitude': '7.5678', 
                'height': '1200'
            },
            'level': {                        # обязательное
                'winter': '1А',
                'summer': '2А',
                'autumn': '1Б',
                'spring': ''
            }
        }
        
        print("Отправляю данные:", json.dumps(correct_data, ensure_ascii=False, indent=2))
        
        response = client.post('/submitData',
                             data=json.dumps(correct_data, ensure_ascii=False),
                             content_type='application/json')
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Тело ответа: {response.data.decode('utf-8')}")
        
        # Если ошибка 500, значит проблема с БД
        # Если 400, значит валидация
        assert response.status_code == 200, f"Ожидался 200, получили {response.status_code}"
        
        data = json.loads(response.data)
        assert data['status'] == 200
        assert data['message'] == 'Success'
        assert isinstance(data['id'], int)
        print(f"✅ Успешно! Создан перевал с ID: {data['id']}")

def test_minimal_valid_data():
    """Тест с минимальными валидными данными"""
    app = create_app()
    
    with app.test_client() as client:
        minimal_data = {
            'beautyTitle': 'пер. ',
            'title': 'Минимальный',
            'user': {
                'email': 'minimal@test.com',
                'fam': 'Минималов',
                'name': 'Мин'
            },
            'coords': {
                'latitude': '45.0',
                'longitude': '7.0',
                'height': '1000'
            },
            'level': {
                'winter': '',
                'summer': '',
                'autumn': '',
                'spring': ''
            }
        }
        
        print("\nОтправляю минимальные данные...")
        response = client.post('/submitData',
                             data=json.dumps(minimal_data),
                             content_type='application/json')
        
        print(f"Статус: {response.status_code}")
        if response.status_code != 200:
            print(f"Ошибка: {response.data}")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 200
        print(f"✅ Минимальные данные приняты! ID: {data['id']}")

def test_missing_beautyTitle():
    """Тест что без beautyTitle будет ошибка"""
    app = create_app()
    
    with app.test_client() as client:
        data_without_beautyTitle = {
            'title': 'Без beautyTitle',
            'user': {
                'email': 'nobeauty@test.com',
                'fam': 'Безкрасоты',
                'name': 'Тест'
            },
            'coords': {
                'latitude': '45.0',
                'longitude': '7.0',
                'height': '1000'
            },
            'level': {
                'summer': '1А'
            }
        }
        
        response = client.post('/submitData',
                             data=json.dumps(data_without_beautyTitle),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        print(f"✅ Корректная ошибка при отсутствии beautyTitle: {data['message']}")
        assert 'beautyTitle' in data['message']