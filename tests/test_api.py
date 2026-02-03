import pytest
from app import create_app
import json
import tempfile
import sqlite3
import atexit
import os

# Глобальная переменная для хранения путей к временным файлам
_temp_files = []

def _cleanup_temp_files():
    """Очистка временных файлов при завершении"""
    for path in _temp_files:
        try:
            if os.path.exists(path):
                os.unlink(path)
        except:
            pass

atexit.register(_cleanup_temp_files)

@pytest.fixture
def client():
    """Фикстура для тестового клиента Flask с тестовой базой данных"""
    # Создаем временную базу данных для тестов
    db_fd, db_path = tempfile.mkstemp()
    _temp_files.append(db_path)
    
    app = create_app()
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    
    # Переопределяем базу данных для тестов
    from app.models import database
    database.db_manager.db_file = db_path
    
    # Создаем тестовые таблицы
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            phone TEXT,
            fam TEXT NOT NULL,
            name TEXT NOT NULL,
            otc TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS perevals (
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
        CREATE TABLE IF NOT EXISTS pereval_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pereval_id INTEGER NOT NULL,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            title TEXT,
            file_path TEXT NOT NULL,
            FOREIGN KEY (pereval_id) REFERENCES perevals(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spr_activities_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pereval_activities (
            pereval_id INTEGER NOT NULL,
            activity_type_id INTEGER NOT NULL,
            PRIMARY KEY (pereval_id, activity_type_id),
            FOREIGN KEY (pereval_id) REFERENCES perevals(id),
            FOREIGN KEY (activity_type_id) REFERENCES spr_activities_types(id)
        )
    ''')
    
    # Тестовые данные
    cursor.execute("INSERT OR IGNORE INTO spr_activities_types (title) VALUES ('пешком')")
    cursor.execute("INSERT OR IGNORE INTO spr_activities_types (title) VALUES ('лыжи')")
    
    conn.commit()
    conn.close()
    os.close(db_fd)
    
    with app.test_client() as client:
        yield client