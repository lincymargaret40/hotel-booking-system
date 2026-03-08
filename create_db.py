import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    room TEXT,
    stay_type TEXT,
    hours INTEGER
)
""")

conn.commit()
conn.close()

print("Database created successfully")