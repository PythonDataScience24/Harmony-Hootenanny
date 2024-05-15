import time
import sqlite3
from datetime import datetime, timedelta
from database import init_db, add_song_to_db, add_song_to_queue, get_db_connection

# Initialize the database using the provided schema

# Add sample users to the database
def add_users():
    users = [
        ("user1", "password_hash1"),
        ("user2", "password_hash2")
    ]
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany('INSERT INTO users (username, password_hash) VALUES (?, ?)', users)
            conn.commit()
            print("Users successfully added to database")
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")

# Add sample songs to the database
def add_songs():
    add_song_to_db("One Love", "Bob Marley", 164, "Bob Marley - One Love.mp3")
    add_song_to_db("Down Under", "Men At Work", 240, "Men At Work - Down Under (Official HD Video).mp3")

# Add sample rooms to the database
def add_rooms():
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
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")

# Add sample queue entries to the database
def add_queues():
    queues = [
        (1, 1, 1),
        (2, 2, 2)
    ]
    for queue in queues:
        add_song_to_queue(queue[0], queue[1], queue[2])

# Populate the database with sample data
def populate_database():
    add_users()
    add_songs()
    add_rooms()
    add_queues()

if __name__ == "__main__":
    init_db()
    populate_database()
    print("Database populated successfully!")
