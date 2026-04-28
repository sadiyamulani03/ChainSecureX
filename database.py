import sqlite3

DB_NAME = "chat.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_message(username, message, timestamp):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)",
        (username, message, timestamp)
    )

    conn.commit()
    conn.close()

def load_messages():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT username, message, timestamp FROM messages")

    rows = cursor.fetchall()
    conn.close()

    return rows
