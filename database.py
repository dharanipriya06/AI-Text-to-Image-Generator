import sqlite3

DB_NAME = "users.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


def register_user(username, email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(username, email, password) VALUES(?,?,?)",
            (username, email, password)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()

    return user


# ==========================
# Prompt History Table
# ==========================

def create_history_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prompt_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        prompt TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_prompt(username, prompt):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO prompt_history(username, prompt) VALUES(?, ?)",
        (username, prompt)
    )

    conn.commit()
    conn.close()


def get_prompt_history(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT prompt FROM prompt_history WHERE username=? ORDER BY id DESC",
        (username,)
    )

    history = cursor.fetchall()

    conn.close()

    return history