import sqlite3
import hashlib

DB_NAME = "MoneyChanger.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()


# ================================
# HASH PASSWORD
# ================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ================================
# REGISTER USER
# ================================
def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        hashed_pw = hash_password(password)
        c.execute("INSERT INTO user(username, password) VALUES (?, ?)",
                  (username, hashed_pw))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False


# ================================
# LOGIN USER
# ================================
def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    hashed_pw = hash_password(password)
    c.execute("SELECT * FROM user WHERE username=? AND password=?",
              (username, hashed_pw))

    result = c.fetchone()
    conn.close()
    return result
