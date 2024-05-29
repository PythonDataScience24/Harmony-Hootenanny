import time
import sqlite3
from datetime import datetime, timedelta
from database import add_song_to_db_queue, init_db, add_song_to_db, get_db_connection

# Initialize the database using the provided schema

# Add sample users to the database
def add_users():
    """
    Add sample users to the database from mockData/users.csv file.

    This function reads the users.csv file, which contains user data in the format:
    user_id, username, password_hash. It then inserts this data into the users table in the database.
    
    """
    with open("./mockData/users.csv", "r") as users_mockfile:
        users = [line.strip().split(",") for line in users_mockfile]
    users.pop(0)
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany('INSERT INTO users (user_id, username, password_hash) VALUES (?, ?, ?)', users)
            conn.commit()
            print("Users successfully added to database")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

# Add sample songs to the database
def add_songs():
    """
    Add sample songs to the database from mockData/songs.csv file.

    This function reads the songs.csv file, which contains song data in the format:
    song_id, src, title, artist, duration. It then inserts this data into the songs table in the database.

    """
    with open("./mockData/songs.csv", "r") as songs_mockfile:
        songs = [line.strip().split(",") for line in songs_mockfile]
    songs.pop(0)
    for song in songs:
        add_song_to_db(song[2], song[3], song[4], song[1])

# Add sample rooms to the database
def add_rooms():
    """
    Add 3 sample rooms to the database

    This function adds 3 sample rooms to the rooms table in the database. The rooms are initialized with the following data:
    room_id, number_of_listeners, session_start_time, session_end_time, session_duration, song_start_time, queue_index.

    """
    now = int(time.time())
    rooms = [
        (1, 10, now, now + 60*60*100, 3600, now, 1),
        (2, 20, now, now + 60*60*100, 7200, now, 2),
        (3, 30, now, now + 60*60*100, 10800, now, 3)
    ]
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany('INSERT INTO rooms (room_id, number_of_listeners, session_start_time, session_end_time, session_duration, song_start_time, queue_index) VALUES (?, ?, ?, ?, ?, ?, ?)', rooms)
            conn.commit()
            print("Rooms successfully added to database")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

# Add sample queue entries to the database
def add_queues():
    """
    Add sample queue entries to the database from mockData/queues.csv file.

    This function reads the queues.csv file, which contains queue data in the format:
    queue_index, song_id, room_id, user_id. It then inserts this data into the queues table in the database.

    """
    with open("./mockData/queues.csv", "r") as queue_mockfile:
        queues = [line.strip().split(",") for line in queue_mockfile]
    queues.pop(0)
    for queue_entry in queues:
        add_song_to_db_queue(queue_entry[1], queue_entry[2], queue_entry[3])

# Add sample user actions to the database
def add_user_actions():
    """
    Add sample user actions to the database from mockData/userActions.csv file.

    This function reads the userActions.csv file, which contains user action data in the format:
    action_id, action_type, action_timestamp, room_id, user_id. It then inserts this data into the user_actions table in the database.
    
    """
    with open("./mockData/userActions.csv", "r") as user_actions_mockfile:
        user_actions = [line.strip().split(",") for line in user_actions_mockfile]
    user_actions.pop(0)  # remove header
    for row in user_actions:
        del row[0]
        row[1] = (datetime.fromtimestamp(float (row[1])/1000))
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany('INSERT INTO user_actions (action_type, action_timestamp, room_id, user_id) VALUES (?, ?, ?, ?)', user_actions)
            conn.commit()
            print("User actions successfully added to database")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

# Update the populate_database function
def populate_database():
    add_users()
    add_songs()
    add_rooms()
    add_queues()
    add_user_actions()

if __name__ == "__main__":
    init_db()
    populate_database()
    print("Database populated successfully!")