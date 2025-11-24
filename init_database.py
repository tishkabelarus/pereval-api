# init_database.py
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    # Получаем путь к базе данных из .env
    database_url = os.getenv('DATABASE_URL', 'sqlite:///pereval.db')
    db_file = database_url.replace('sqlite:///', '')
    
    print(f"Создание базы данных: {db_file}")
    
    # Удаляем старую базу если существует
    if os.path.exists(db_file):
        os.remove(db_file)
        print("Старая база данных удалена")
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Включаем поддержку внешних ключей
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Читаем и выполняем SQL скрипт
        with open('migrations/init_tables.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Выполняем команды по очереди
        commands = sql_script.split(';')
        
        for command in commands:
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    print(f"Выполнено: {command[:50]}...")
                except Exception as e:
                    print(f"Ошибка в команде: {e}")
        
        conn.commit()
        
        # Проверяем созданные таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("\nСозданные таблицы:")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        
        print(f"\nБаза данных успешно создана: {db_file}")
        
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")

if __name__ == '__main__':
    init_database()