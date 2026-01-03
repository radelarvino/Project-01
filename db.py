import sqlite3


DB_NAME = "nasi_padang_project.db"

def get_connections():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def execute(query, params=()):
    with get_connections() as conn:
        conn.execute(query, params)

def fetch_one(query, params=()):
    with get_connections() as conn:
        cur = conn.execute(query, params)
        return cur.fetchone()

def fetch_all(query, params=()):
    with get_connections() as conn:
        cur = conn.execute(query, params)
        return cur.fetchall()
