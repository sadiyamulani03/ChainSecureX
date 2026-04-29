import sqlite3

DB_NAME = "chat.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create base table (if not exists)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT,
        timestamp TEXT
    )
    """)

    # Check existing columns
    cursor.execute("PRAGMA table_info(messages)")
    columns = [col[1] for col in cursor.fetchall()]

    # Add missing columns safely
    if "hash" not in columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN hash TEXT")

    if "prev_hash" not in columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN prev_hash TEXT")

    conn.commit()
    conn.close()


def get_last_hash():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT hash FROM messages ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        return row[0] if row and row[0] else "0"
    except:
        return "0"
    finally:
        conn.close()


def save_message(username, message, timestamp, msg_hash, prev_hash):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (username, message, timestamp, hash, prev_hash) VALUES (?, ?, ?, ?, ?)",
        (username, message, timestamp, msg_hash, prev_hash)
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
