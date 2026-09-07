import sqlite3

def get_connection():
    connection = sqlite3.connect('app.db', check_same_thread=False)
    connection.row_factory = sqlite3.Row
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