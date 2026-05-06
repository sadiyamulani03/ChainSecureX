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
        timestamp TEXT,
        hash TEXT,
        prev_hash TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_message(username, message, timestamp, hash_value, prev_hash):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # HARD duplicate prevention
    cursor.execute("""
        SELECT 1 FROM messages
        WHERE username=? AND message=? AND timestamp=?
    """, (username, message, timestamp))

    if cursor.fetchone():
        conn.close()
        return

    cursor.execute("""
        INSERT INTO messages (username, message, timestamp, hash, prev_hash)
        VALUES (?, ?, ?, ?, ?)
    """, (username, message, timestamp, hash_value, prev_hash))

    conn.commit()
    conn.close()

def load_messages():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, message, timestamp
        FROM messages
        ORDER BY id ASC
    """)

    data = cursor.fetchall()
    conn.close()
    return data

def get_last_hash():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT hash FROM messages ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else "0"
