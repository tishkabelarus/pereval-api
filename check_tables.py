import sqlite3

conn = sqlite3.connect('pereval.db')
cursor = conn.cursor()

# Проверим таблицы
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("Таблицы в базе:")
for table in tables:
    print(f"  - {table[0]}")

conn.close()