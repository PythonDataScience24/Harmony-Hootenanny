# database.py

import sqlite3
from contextlib import contextmanager
import time

# Create a context manager for database connections
@contextmanager
def get_db_connection():
    """initializes a connection to the sqlite database and handles closing the connection after it is no longer used.

    Yields:
        Connection: use .cursor().execute(query) to execute queries on the connection object.
    """
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    # print("Successfully connected to database")
    try:
        yield conn
    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        conn.close()
        # print("con closed")

    
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

def add_song_to_db(title:str, artist:str, duration:int, fileName:str):
    """
    Add a song to the database
    """
    try:
        with get_db_connection() as conn:
            conn.cursor().execute("INSERT INTO songs (title, artist, duration, src) VALUES (?, ?, ?, ?)",\
                           (title, artist, duration, fileName))
            conn.commit()
            # print("Song successfully added to database")
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")

def add_song_to_queue(songId:int, roomId:int, userId:int):
    """
    Add a song to the queue
    """
    try:
        with get_db_connection() as conn:
            conn.cursor().execute("INSERT INTO queues (song_id, room_id, user_id) VALUES (?, ?, ?)",\
                           (songId, roomId, userId))
            conn.commit()
            # print("Song successfully added to queue")
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")

def remove_song_from_queue(queueIndex:int):
    """
    Remove a song from the queue
    """
    try:
        with get_db_connection() as conn:
            conn.cursor().execute(f"DELETE FROM queues WHERE queue_index = ?",(queueIndex,))
            conn.commit()
            # print("Song successfully removed from queue")
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")

def get_queue(roomId:int):
    """
    Get the song queue of a specified room
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor().execute("SELECT title, artist, duration FROM queues LEFT JOIN songs USING(song_id) WHERE room_id = ?",(roomId,))
            rows = cursor.fetchall()
            # Convert the results into the desired format
            song_queue = [
                {"title": row[0], "artist": row[1], "duration": row[2]}
                for row in rows
            ]
            # print("Queue successfully selected")
            return song_queue
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")

def get_current_song(roomId:int) -> dict:
    try:
        with get_db_connection() as conn:
            result = conn.cursor().execute('SELECT \
                                    r.song_start_time, \
                                    s.title AS song_title, \
                                    s.artist AS song_artist, \
                                    s.src AS file_path, \
                                    r.queue_index as queue_index \
                                    FROM rooms AS r \
                                    INNER JOIN queues AS q ON r.queue_index = q.queue_index \
                                    INNER JOIN songs AS s ON q.song_id = s.song_id \
                                    INNER JOIN users AS u ON q.user_id = u.user_id \
                                    WHERE r.room_id = ?;'
                                  , (roomId,))
            current_data = result.fetchone()
            currently_playing: dict = {
                "title":current_data[1], 
                "artist":current_data[2], 
                "filename":current_data[3], 
                "progress":int(time.time())-current_data[0], 
                "queue_index":current_data[4]
            }   
            return currently_playing
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")

def get_next_song(roomId: int) -> dict:
    try:
        with get_db_connection() as conn:
            result = conn.cursor().execute('SELECT \
                                    q.queue_index, \
                                    s.title AS song_title, \
                                    s.artist AS song_artist, \
                                    s.duration AS song_duration, \
                                    s.src AS file_path \
                                    FROM queues AS q \
                                    INNER JOIN songs AS s ON q.song_id = s.song_id \
                                    WHERE q.room_id = ? AND q.queue_index > \
                                    (SELECT queue_index FROM rooms WHERE room_id = ?) \
                                    ORDER BY q.queue_index ASC LIMIT 1;', (roomId, roomId))
            next_data = result.fetchone()
            if next_data:
                next_song: dict = {
                    "queue_index": next_data[0],
                    "title": next_data[1],
                    "artist": next_data[2],
                    "duration": next_data[3],
                    "filename": next_data[4]
                }
                return next_song
            else:
                return None
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")
        return None

if __name__ == "__main__":
    """
    use for developing or setting up the database.
    """
    # init_db() # if no database.db file exists or schema.sql was updated