import sqlite3
import hashlib

DB_NAME = "usernameAplikasi.db"

# ================== UTIL HASH ==================
def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

# ================== KONEKSI DB ==================
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

# ================== USER CHECK ==================
def user_exists(username):
    conn = get_connection()
    cur = conn.cursor()

    hashed_username = hash_text(username)

    cur.execute(
        "SELECT 1 FROM users WHERE username = ?",
        (hashed_username,)
    )
    result = cur.fetchone()
    conn.close()
    return result is not None

# ================== ADD USER ==================
def add_user(username, password):
    try:
        conn = get_connection()
        cur = conn.cursor()

        hashed_username = hash_text(username)
        hashed_password = hash_text(password)

        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (hashed_username, hashed_password)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# ================== LOGIN VALIDATION ==================
def validate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    hashed_username = hash_text(username)
    hashed_password = hash_text(password)

    cur.execute(
        "SELECT 1 FROM users WHERE username = ? AND password = ?",
        (hashed_username, hashed_password)
    )
    result = cur.fetchone()
    conn.close()
    return result is not None

# ================== UPDATE PASSWORD ==================
def update_password(username, new_password):
    if not user_exists(username):
        return False

    conn = get_connection()
    cur = conn.cursor()

    hashed_username = hash_text(username)
    hashed_password = hash_text(new_password)

    cur.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (hashed_password, hashed_username)
    )
    conn.commit()
    conn.close()
    return True

# ================== UPDATE USERNAME ==================
def update_username(old_username, new_username):
    conn = get_connection()
    cur = conn.cursor()

    old_hashed = hash_text(old_username)
    new_hashed = hash_text(new_username)

    cur.execute(
        "SELECT 1 FROM users WHERE username = ?",
        (new_hashed,)
    )
    if cur.fetchone():
        conn.close()
        return False

    cur.execute(
        "UPDATE users SET username = ? WHERE username = ?",
        (new_hashed, old_hashed)
    )

    conn.commit()
    conn.close()
    return True

# ================== DELETE USER ==================
def delete_user(username):
    conn = get_connection()
    cur = conn.cursor()

    hashed_username = hash_text(username)

    cur.execute(
        "DELETE FROM users WHERE username = ?",
        (hashed_username,)
    )
    conn.commit()
    conn.close()
