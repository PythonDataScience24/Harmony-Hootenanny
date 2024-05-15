# database.py

import sqlite3
from contextlib import contextmanager

# Create a context manager for database connections
@contextmanager
def get_db_connection():
    """initializes a connection to the sqlite database and handles closing the connection after it is no longer used.

    Yields:
        Connection: use .cursor().execute(query) to execute queries on the connection object.
    """
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    print("Successfully connected to database")
    try:
        yield conn
    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        conn.close()
        print("con closed")

    
def init_db() -> None:
    """
    intializes database using the schema given in a local file 'schema.sql'
    """
    try:
        with get_db_connection() as conn, open('schema.sql', mode='r') as schema:
            conn.cursor().executescript(schema.read())
            conn.commit()
            print("Database initialized")
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")
    finally:
        print("initialization done")

def get_user() -> list[any]:
    """
    example of get query
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor().execute("SELECT * FROM rooms")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")


def set_username(username) -> None:
    """
    example of set query
    """
    try:
        with get_db_connection() as conn:
            conn.cursor().execute("UPDATE users SET username = ? WHERE username = ?", (username, username,))
            conn.commit() # important to commit on UPDATE, INSERT, DELETE, etc.
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")

def add_song_to_db(fileName:str, title:str, artist:str, duration:int):
    pass

def add_song_to_queue(songId:int, roomId:int, userId:int):
    pass

def remove_song_from_queue(queueIndex:int):
    pass

def get_queue(roomId:int):
    pass

def get_current_song(roomId:int):
    pass

if __name__ == "__main__":
    """
    use for developing or setting up the database.
    """
    init_db() # if no database.db file exists or schema.sql was updated