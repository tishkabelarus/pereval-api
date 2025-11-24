import sqlite3
import os
import logging
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        # Получаем настройки из переменных окружения
        self.db_host = os.getenv('FSTR_DB_HOST', 'localhost')
        self.db_port = os.getenv('FSTR_DB_PORT', '5432') 
        self.db_login = os.getenv('FSTR_DB_LOGIN', 'postgres')
        self.db_pass = os.getenv('FSTR_DB_PASS', 'password')
        self.db_name = os.getenv('FSTR_DB_NAME', 'pereval')
        
        # Для SQLite используем файл, но логируем "подключение" с переменными окружения
        self.db_file = 'pereval.db'
        
        print("🔧 Настройки базы данных из переменных окружения:")
        print(f"   Host: {self.db_host}")
        print(f"   Port: {self.db_port}")
        print(f"   Login: {self.db_login}")
        print(f"   Database: {self.db_name}")
        print(f"   Actual DB file: {self.db_file}")
        
    def add_pereval(self, data):
        try:
            print(f"🎯 Подключаемся к базе (используется SQLite: {self.db_file})")
            
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Создаем пользователя
            user_data = data.get('user', {})
            print(f"👤 Создаем пользователя: {user_data.get('email')}")
            
            cursor.execute(
                "INSERT INTO users (email, phone, fam, name, otc) VALUES (?, ?, ?, ?, ?)",
                (user_data.get('email'), user_data.get('phone'), user_data.get('fam'), 
                 user_data.get('name'), user_data.get('otc'))
            )
            user_id = cursor.lastrowid
            print(f"✅ Пользователь создан: {user_id}")
            
            # Добавляем перевал
            cursor.execute(
                """INSERT INTO perevals 
                (beauty_title, title, other_titles, connect, 
                 latitude, longitude, height, user_id, area_id,
                 level_winter, level_summer, level_autumn, level_spring, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'new')""",
                (
                    data.get('beautyTitle'), data.get('title'), data.get('other_titles'),
                    data.get('connect'), float(data.get('coords', {}).get('latitude', 0)),
                    float(data.get('coords', {}).get('longitude', 0)),
                    int(data.get('coords', {}).get('height', 0)), user_id, 1,
                    data.get('level', {}).get('winter'), data.get('level', {}).get('summer'),
                    data.get('level', {}).get('autumn'), data.get('level', {}).get('spring')
                )
            )
            pereval_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            print(f"🎉 УСПЕХ! Перевал создан с ID: {pereval_id}")
            return {'status': 200, 'message': 'Success', 'id': pereval_id}
            
        except Exception as e:
            print(f"❌ ОШИБКА: {e}")
            return {'status': 500, 'message': f'Database error: {str(e)}', 'id': None}

db_manager = DatabaseManager()