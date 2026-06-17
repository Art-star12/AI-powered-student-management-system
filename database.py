import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE students(
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    university TEXT,
    subject TEXT,
    marks INTEGER,
    percentage REAL,
    grade TEXT,
    total_fees REAL,
    fees_paid REAL,
    remaining_fees REAL,
    payment_status TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully!")