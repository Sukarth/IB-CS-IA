import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent # repo root
DB_PATH = BASE_DIR / 'instance' / 'app.sqlite'
SCHEMA_PATH = Path(__file__).resolve().parent / 'schema.sql'

def init_db():
    connection = get_connection()
    with open(SCHEMA_PATH, 'r') as f:
        connection.executescript(f.read())
    connection.close()

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def execute(sql, params=()):
    connection = get_connection()
    cursor = connection.execute(sql, params)
    connection.commit()
    last_row_id = cursor.lastrowid
    connection.close()
    return last_row_id

def query(sql, params=()):
    connection = get_connection()
    rows = connection.execute(sql, params).fetchall()
    connection.close()
    return rows

def query_one(sql, params=()):
    connection = get_connection()
    row = connection.execute(sql, params).fetchone()
    connection.close()
    return row