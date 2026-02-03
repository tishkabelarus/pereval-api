import pytest
import sqlite3
import tempfile
import os
import atexit

# Глобальная переменная для хранения путей к временным файлам
_temp_db_files = []

def _cleanup_db_files():
    """Очистка временных файлов БД"""
    for path in _temp_db_files:
        try:
            if os.path.exists(path):
                os.unlink(path)
        except:
            pass

atexit.register(_cleanup_db_files)

@pytest.fixture
def db_manager():
    """Фикстура для создания DatabaseManager с тестовой базой"""
    # Создаем временный файл для базы данных
    import tempfile
    db_fd, db_path = tempfile.mkstemp()
    _temp_db_files.append(db_path)
    
    # Импортируем здесь чтобы избежать циклических импортов
    from app.models.database import DatabaseManager
    
    manager = DatabaseManager()
    manager.db_file = db_path
    
    # Создаем тестовую базу
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Создаем таблицы
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            phone TEXT,
            fam TEXT NOT NULL,
            name TEXT NOT NULL,
            otc TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE perevals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            beauty_title TEXT,
            title TEXT NOT NULL,
            other_titles TEXT,
            connect TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            height INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            area_id INTEGER DEFAULT 1,
            level_winter TEXT,
            level_summer TEXT,
            level_autumn TEXT,
            level_spring TEXT,
            status TEXT DEFAULT 'new',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE pereval_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pereval_id INTEGER NOT NULL,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            title TEXT,
            file_path TEXT NOT NULL,
            FOREIGN KEY (pereval_id) REFERENCES perevals(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE spr_activities_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE pereval_activities (
            pereval_id INTEGER NOT NULL,
            activity_type_id INTEGER NOT NULL,
            PRIMARY KEY (pereval_id, activity_type_id),
            FOREIGN KEY (pereval_id) REFERENCES perevals(id),
            FOREIGN KEY (activity_type_id) REFERENCES spr_activities_types(id)
        )
    ''')
    
    # Тестовые данные
    cursor.execute("INSERT INTO spr_activities_types (title) VALUES ('пешком')")
    cursor.execute("INSERT INTO spr_activities_types (title) VALUES ('лыжи')")
    cursor.execute("INSERT INTO spr_activities_types (title) VALUES ('велосипед')")
    
    conn.commit()
    conn.close()
    os.close(db_fd)
    
    yield manager

def test_add_pereval(db_manager):
    """Тест добавления перевала"""
    test_data = {
        'beautyTitle': 'пер. ',
        'title': 'Тестовый перевал',
        'other_titles': 'Тест',
        'connect': 'соединяет долины',
        'user': {
            'email': 'test@example.com',
            'phone': '79031234567',
            'fam': 'Иванов',
            'name': 'Петр',
            'otc': 'Сергеевич'
        },
        'coords': {
            'latitude': '45.3842',
            'longitude': '7.1525',
            'height': '1200'
        },
        'level': {
            'winter': '',
            'summer': '1А',
            'autumn': '1А',
            'spring': ''
        }
    }
    
    result = db_manager.add_pereval(test_data)
    
    assert result['status'] == 200
    assert result['message'] == 'Success'
    assert result['id'] is not None
    assert isinstance(result['id'], int)

def test_get_pereval(db_manager):
    """Тест получения перевала по ID"""
    # Сначала добавляем перевал
    test_data = {
        'beautyTitle': 'пер. ',
        'title': 'Тестовый перевал',
        'user': {
            'email': 'test@example.com',
            'fam': 'Иванов',
            'name': 'Петр'
        },
        'coords': {
            'latitude': '45.3842',
            'longitude': '7.1525',
            'height': '1200'
        },
        'level': {
            'summer': '1А',
            'autumn': '1А'
        }
    }
    
    add_result = db_manager.add_pereval(test_data)
    pereval_id = add_result['id']
    
    # Получаем перевал
    pereval = db_manager.get_pereval(pereval_id)
    
    assert pereval is not None
    assert pereval['id'] == pereval_id
    assert pereval['title'] == 'Тестовый перевал'
    assert pereval['beautyTitle'] == 'пер. '
    assert pereval['status'] == 'new'
    
    # Проверяем пользователя
    assert 'user' in pereval
    assert pereval['user']['email'] == 'test@example.com'
    assert pereval['user']['fam'] == 'Иванов'
    assert pereval['user']['name'] == 'Петр'
    
    # Проверяем координаты
    assert 'coords' in pereval
    assert str(pereval['coords']['latitude']) == '45.3842'
    assert str(pereval['coords']['longitude']) == '7.1525'
    assert str(pereval['coords']['height']) == '1200'
    
    # Проверяем уровень
    assert 'level' in pereval
    assert pereval['level']['summer'] == '1А'
    assert pereval['level']['autumn'] == '1А'

def test_update_pereval(db_manager):
    """Тест обновления перевала"""
    # Сначала добавляем перевал
    test_data = {
        'beautyTitle': 'пер. ',
        'title': 'Тестовый перевал',
        'user': {
            'email': 'test@example.com',
            'fam': 'Иванов',
            'name': 'Петр'
        },
        'coords': {
            'latitude': '45.3842',
            'longitude': '7.1525',
            'height': '1200'
        },
        'level': {
            'summer': '1А'
        }
    }
    
    add_result = db_manager.add_pereval(test_data)
    pereval_id = add_result['id']
    
    # Обновляем перевал
    update_data = {
        'title': 'Обновленное название',
        'level': {
            'summer': '2А',
            'autumn': '2А'
        }
    }
    
    update_result = db_manager.update_pereval(pereval_id, update_data)
    
    assert update_result['state'] == 1
    assert update_result['message'] == 'Success'
    
    # Проверяем что данные обновились
    pereval = db_manager.get_pereval(pereval_id)
    assert pereval['title'] == 'Обновленное название'
    assert pereval['level']['summer'] == '2А'
    assert pereval['level']['autumn'] == '2А'

def test_update_pereval_not_found(db_manager):
    """Тест обновления несуществующего перевала"""
    update_result = db_manager.update_pereval(999, {'title': 'Новое название'})
    assert update_result['state'] == 0
    assert 'not found' in update_result['message'].lower()

def test_get_pereval_by_user_email(db_manager):
    """Тест получения перевалов пользователя по email"""
    # Добавляем несколько перевалов для одного пользователя
    user_email = 'user1@example.com'
    
    for i in range(3):
        test_data = {
            'title': f'Перевал {i}',
            'user': {
                'email': user_email,
                'fam': 'Иванов',
                'name': 'Петр'
            },
            'coords': {
                'latitude': '45.3842',
                'longitude': '7.1525',
                'height': '1200'
            },
            'level': {
                'summer': '1А'
            }
        }
        db_manager.add_pereval(test_data)
    
    # Получаем перевалы пользователя
    perevals = db_manager.get_pereval_by_user_email(user_email)
    
    assert len(perevals) == 3
    for pereval in perevals:
        assert 'Перевал' in pereval['title']
        assert pereval['status'] == 'new'

def test_get_pereval_not_found(db_manager):
    """Тест получения несуществующего перевала"""
    pereval = db_manager.get_pereval(999)
    assert pereval is None

def test_empty_user_email(db_manager):
    """Тест получения перевалов для несуществующего email"""
    perevals = db_manager.get_pereval_by_user_email('nonexistent@example.com')
    assert perevals == []