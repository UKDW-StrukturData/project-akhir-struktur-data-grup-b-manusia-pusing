import sqlite3

DB_NAME = "usernameAplikasi.db"


# Pembuatan database sistem dibantu oleh GPT
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def user_exists(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    result = cur.fetchone()
    conn.close()
    return result is not None

def add_user(username, password):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def validate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    result = cur.fetchone()
    conn.close()
    return result is not None

def update_username(old_username, new_username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM users WHERE username = ?", (new_username,))
    if cur.fetchone():
        conn.close()
        return False

    cur.execute(
        "UPDATE users SET username = ? WHERE username = ?",
        (new_username, old_username)
    )

    conn.commit()
    conn.close()
    return True

def delete_user(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
