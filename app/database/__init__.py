import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent # repo root
DB_PATH = BASE_DIR / 'instance' / 'app.sqlite'
SCHEMA_PATH = Path(__file__).resolve().parent / 'schema.sql'

def init_db():
    connection = get_connection()
    try:
        with open(SCHEMA_PATH, 'r') as f:
            connection.executescript(f.read())
    finally:
        connection.close()

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def execute(sql, params=()):
    connection = get_connection()
    try:
        cursor = connection.execute(sql, params)
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()

def query(sql, params=()):
    connection = get_connection()
    try:
        return connection.execute(sql, params).fetchall()
    finally:
        connection.close()

def query_one(sql, params=()):
    connection = get_connection()
    try:
        return connection.execute(sql, params).fetchone()
    finally:
        connection.close()