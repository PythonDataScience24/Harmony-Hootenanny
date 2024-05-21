import time
import sqlite3
from datetime import datetime, timedelta
from database import init_db, add_song_to_db, add_song_to_queue, get_db_connection

# Initialize the database using the provided schema

# Add sample users to the database
def add_users():
    users_mockfile = open("./mockData/users.csv", "r")
    users = []
    for line in users_mockfile:
        line = line[0:-2] # to skip \n at every end of line
        user = line.split(",")
        users.append(user)
    users.pop(0)
    try:
        for user in users:
            with get_db_connection() as conn:
                conn.cursor().execute(f'INSERT INTO users (user_id, username, password_hash) VALUES (\'{user[0]}\', \'{user[1]}\', \'{user[2]}\')')
                conn.commit()
                print("Users successfully added to database")
    except sqlite3.Error as e:
        print(f"SQLite error code: {e.sqlite_errorcode}")
        print(f"SQLite error name: {e.sqlite_errorname}")

# Add sample songs to the database
def add_songs():
    songs_mockfile = open("./mockData/songs.csv", "r")
    songs = []
    for line in songs_mockfile:
        line = line[0:-2] # to skip \n at every end of line
        song = line.split(",")
        songs.append(song)
    songs.pop(0)
    for song in songs:
        add_song_to_db(song[2], song[3], song[4], song[1])
    # add_song_to_db("One Love", "Bob Marley", 164, "Bob Marley - One Love.mp3")
    # add_song_to_db("Down Under", "Men At Work", 240, "Men At Work - Down Under (Official HD Video).mp3")

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
    queue_mockfile = open("./mockData/queues.csv", "r")
    queues = []
    for line in queue_mockfile:
        line = line[0:-2] # to skip \n at every end of line
        queue_entry = line.split(",")
        queues.append(queue_entry)
    queues.pop(0)
    for queue_entry in queues:
        add_song_to_queue(queue_entry[1], queue_entry[2], queue_entry[3])

# Populate the database with sample data
def populate_database():
    # add_users()
    # add_songs()
    # add_rooms()
    # add_queues()
    pass

if __name__ == "__main__":
    init_db()
    populate_database()
    print("Database populated successfully!")
