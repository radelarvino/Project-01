import sqlite3

DB_PATH = "nasi_padang_project.db"
SCHEMA_PATH = "sql/schema.sql"
SEED_PATH =  "sql/seed.sql"

def run_sql_file(cursor, path):
    with open(path, "r") as f:
        cursor.executescript(f.read())

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    run_sql_file(cursor, SCHEMA_PATH)
    run_sql_file(cursor, SEED_PATH)

    conn.commit()
    conn.close()
