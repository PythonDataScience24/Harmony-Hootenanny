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

def get_user_id(username):
    """
    Retrieves the user ID for the given username from the database.

    Args:
        username (str): The username to look up.

    Returns:
        int or None: The user ID if found, otherwise None.

    This function queries the database for the user ID corresponding to the provided username.
    If a match is found, it returns the user ID; otherwise, it returns None.
    """
    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result[0] if result else None
    
def add_song_to_db(title:str, artist:str, duration:int, filename:str):
    """
    Add a song to the database.

    Args:
        title (str): Song title.
        artist (str): Song artist.
        duration (int): Song duration in seconds.
        filename (str): Song file name.

    Returns:
        None

    Raises:
        sqlite3.Error: Database interaction error.
    """
    try:
        with get_db_connection() as conn:
            conn.cursor().execute("INSERT INTO songs (title, artist, duration, src) VALUES (?, ?, ?, ?)",\
                           (title, artist, duration, filename))
            conn.commit()
            # print("Song successfully added to database")
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")

def add_song_to_db_queue(song_Id:int, room_Id:int, user_Id:int):
    """
    Add a song to the queue.

    Args:
        song_Id (int): Song ID.
        room_Id (int): Room ID.
        user_Id (int): User ID.

    Returns:
        None

    Raises:
        sqlite3.Error: Database interaction error.
    """
    try:
        with get_db_connection() as conn:
            conn.cursor().execute("INSERT INTO queues (song_id, room_id, user_id) VALUES (?, ?, ?)",\
                           (song_Id, room_Id, user_Id))
            conn.commit()
            # print("Song successfully added to queue")
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")

def remove_song_from_queue(queue_index:int):
    """
    Remove a song from the queue.

    Args:
        queue_index (int): Queue index of the song.

    Returns:
        None

    Raises:
        sqlite3.Error: Database interaction error.
    """
    try:
        with get_db_connection() as conn:
            conn.cursor().execute(f"DELETE FROM queues WHERE queue_index = ?",(queue_index,))
            conn.commit()
            # print("Song successfully removed from queue")
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")

def get_queue(room_Id:int):
    """
    Get the song queue for a room.

    Args:
        room_Id (int): Room ID.

    Returns:
        list of dict: List of songs with title, artist, and duration.

    Raises:
        sqlite3.Error: Database interaction error.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor().execute("SELECT title, artist, duration FROM queues LEFT JOIN songs USING(song_id) WHERE room_id = ?",(room_Id,))
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

def get_current_song(room_Id:int) -> dict:
    """
    Get the currently playing song in a room.

    Args:
        room_Id (int): Room ID.

    Returns:
        dict: Currently playing song details including title, artist, filename, progress, and queue index.

    Raises:
        sqlite3.Error: Database interaction error.
    """
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
                                  , (room_Id,))
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

def get_song_by_id(song_Id:int):
    """
    Get a song by ID.

    Args:
        song_Id (int): Song ID.

    Returns:
        dict: Song details including title, artist, source, and duration.

    Raises:
        sqlite3.Error: Database interaction error.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor().execute("SELECT title, artist, src, duration FROM songs WHERE song_id = ?",(song_Id,))
            row = cursor.fetchone()
            if row:
                # Convert the results into the desired format
                song = {
                    "title": row[0], 
                    "artist": row[1], 
                    "src": row[2], 
                    "duration": row[3]
                }
                # print("Song successfully selected")
                return song
            else:
                return print("SongID not found in database")
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")

def get_song_id_by_name(song_name:str):
    """
    Get a song ID by song Title.

    Args:
        song_name (str): Song Title.

    Returns:
        dict: Song details including title, artist, source, and duration.

    Raises:
        sqlite3.Error: Database interaction error.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Add wildcards around the song_name for LIKE query
            song_name_with_wildcards = f"%{song_name}%"
            cursor.execute("SELECT song_id FROM songs WHERE title LIKE ?", (song_name_with_wildcards,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return print("Song name not found in database")
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")


def add_user_action(action_type: str, room_id: int, username: str):
    """
    Add a user action to the user_actions table.

    Args:
        action_type (str): Type of user action (e.g., 'join_room', 'leave_room', etc.).
        room_id (int): ID of the room associated with the action.
        username (str): Username of the user performing the action.

    Returns:
        None

    Raises:
        sqlite3.Error: Database interaction error.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            user_id = cursor.fetchone()
            
            if user_id is None:
                print(f"User with username '{username}' not found")
                return
            
            user_id = user_id[0]  # Extract user_id from the fetched tuple

            cursor.execute(
                "INSERT INTO user_actions (action_type, room_id, user_id) VALUES (?, ?, ?)",
                (action_type, room_id, user_id)
            )
            conn.commit()
            print("User action successfully added to database")
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")

if __name__ == "__main__":
    """
    Main entry point for developing or setting up the database.
    Uncomment the init_db() call to initialize the database schema.

    Usage:
        Run this script directly to initialize the database or perform setup tasks.
    """
    # init_db()  # Uncomment to initialize the database if no database.db file exists or if schema.sql was updated