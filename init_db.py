import sqlite3

DB_NAME = "monuments.db"

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# Удаляем старую таблицу, если она существует
c.execute("DROP TABLE IF EXISTS monuments")

# Создаём новую таблицу с колонкой image
c.execute('''
CREATE TABLE monuments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    price REAL NOT NULL,
    image TEXT
)
''')

conn.commit()
conn.close()
print("База monuments.db пересоздана успешно!")