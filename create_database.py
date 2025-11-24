import sqlite3
import os

print("Создаем базу данных...")

# Удаляем если существует
if os.path.exists('pereval.db'):
    os.remove('pereval.db')

conn = sqlite3.connect('pereval.db')
cursor = conn.cursor()

print("Создаем таблицы...")

# Таблица пользователей
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

# Таблица перевалов
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

# Таблица изображений
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

# Таблица активностей
cursor.execute('''
CREATE TABLE spr_activities_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
)
''')

# Связующая таблица
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

conn.commit()
conn.close()

print("База данных создана успешно!")
print("Таблицы: users, perevals, pereval_images, spr_activities_types, pereval_activities")

# Проверим
conn = sqlite3.connect('pereval.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Созданные таблицы:", [table[0] for table in tables])
conn.close()