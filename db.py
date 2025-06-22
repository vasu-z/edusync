import sqlite3

def connect():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()

    c.execute(""" CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT,
            dob TEXT,
            gender TEXT,
            address TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            sid TEXT,
            subject TEXT,
            marks INTEGER
        )
    """)

    conn.commit()
    conn.close()
