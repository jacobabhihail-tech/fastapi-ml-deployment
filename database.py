import sqlite3

# Connect to DB (creates file automatically)
conn = sqlite3.connect("predictions.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    balance REAL,
    prediction INTEGER,
    probability REAL
)
""")

conn.commit()