import sqlite3
from sglite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f'Connected to {db_file}, sqlite version: {sqlite.version}')
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.colse()


