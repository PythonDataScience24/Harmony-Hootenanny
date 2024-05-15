from database import get_current_song, get_queue, get_next_song
from .extensions import socketio
from flask_socketio import emit, join_room, leave_room
from flask import request
from .modules.songcompletionchecker import SongScheduler
import time

# Initialize an empty dictionary to store active users in each room
active_users_by_room = {}
sid_to_user = {}
schedulers = {}  # Store schedulers for each room

@socketio.on("connect")
def handle_connect():
    print("client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("client disconnected")
    room_id = 0
    username_left = sid_to_user[request.sid]
    for key, menge in active_users_by_room.items():
        for username in menge:
            if username_left == username:
                room_id = key 


    active_users_by_room[key].remove(username_left)
    del sid_to_user[request.sid]

    leave_room(room_id, request.sid)
    emit("active_users", {"users":list(active_users_by_room[room_id])}, room=room_id)

@socketio.on("join_room")
def handle_join_room(room_id: int, username: str):
    # Add the user to the room in the database (if needed)
    # Example: UserRoom.create(user_id=user_id, room_id=room_id)
    print(get_queue(room_id))

    sid_to_user[request.sid] = username
    join_room(room_id, request.sid)
    # Add the user's request.sid to the active users list for the room
    if room_id not in active_users_by_room:
        active_users_by_room[room_id] = set()
    active_users_by_room[room_id].add(username)

    # Emit "active_users" event to all users in the same room
    emit("active_users", {"users": list(active_users_by_room[room_id])}, to=room_id)

    # Create new SongScheduler if room does not already have one
    if room_id not in schedulers:
        schedulers[room_id] = SongScheduler(room_id, socketio)
        schedulers[room_id].start_scheduler()

    currently_playing = get_current_song(room_id)
    if currently_playing and 'duration' in currently_playing:
        start_song(room_id, currently_playing)
    else:
        emit("currently_playing", {"track": None, "progress": 0}, room=request.sid)

    emit("song_queue", {"queue": get_queue(room_id)}, room=request.sid)

    #emit("currently_playing", get_current_song(room_id), room=request.sid)
    #emit("active_users", {"users": list(active_users_by_room[room_id])}, room=room_id)

def start_song(room_id, song):
    if 'duration' in song:
        start_time = time.time()
        duration = song['duration']
        schedulers[room_id].add_song(start_time, duration)
        emit("currently_playing", {"track": song['filename'], "progress": 0}, room=room_id)
    else:
        print(f"Error: Song data missing 'duration' key for room_id: {room_id}")



@socketio.on("control")
def handle_control(control: str):
    pass
@socketio.on("queue")
def handle_user_join(filename: str):
    pass

def next_song():
    emit("currently_playing", {"track": currently_playing, "progress": progress}, room=request.sid)



    """

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined.")
    users[username] = request.sid

@socketio.on("new_message")
def handle_new_message(message):
    print(f"new message: {message}")
    username = None
    for user in users:
        if users[user] == request.sid:
            username = user
    emit("chat", {"message": message, "username": username}, broadcast=True)
    """