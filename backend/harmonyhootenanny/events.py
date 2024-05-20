
from harmonyhootenanny.modules.SongScheduler import SongScheduler
from database import get_current_song, get_queue
from .extensions import socketio
from flask_socketio import emit, join_room, leave_room
from flask import request

# Initialize an empty dictionary to store active users in each room
active_users_by_room = {}  # {room_id: {username1, username2, ...}}
sid_to_user = {}  # {socket_id: username}
song_schedulers: dict[int, SongScheduler] = {}  # {room_id: SongScheduler instance}

@socketio.on("connect")
def handle_connect():
    """
    Handles client connection.

    This function is called when a client connects to the Socket.IO server.
    """
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    """
    Handles client disconnection.

    This function is called when a client disconnects from the Socket.IO server.
    """
    print("Client disconnected")
    room_id = 0
    print(active_users_by_room, sid_to_user)
    username_left = sid_to_user[request.sid]

    # Find the room ID where the user was active
    for key, users_set in active_users_by_room.items():
        if username_left in users_set:
            room_id = key
            break

    # Remove the user from the active users set and delete their socket ID
    active_users_by_room[room_id].remove(username_left)
    del sid_to_user[request.sid]

    print(active_users_by_room, sid_to_user)

    # Leave the room and handle song playback
    leave_room(room_id, request.sid)
    handle_play_song(room_id)

    # Emit updated active users list to the room
    emit("active_users", {"users": list(active_users_by_room[room_id])}, room=room_id)
    print("Emitted active users and played song")


@socketio.on("join_room")
def handle_join_room(room_id: int, username: str):
   
    """
    Handles a user joining a room.

    Args:
        room_id (int): The unique identifier for the room.
        username (str): The username of the joining user.

    Notes:
        - Creates a SongScheduler instance for the room if it doesn't exist.
        - Adds the user to the active users list for the room.
        - Associates the user's socket ID with their username.
        - Joins the user to the WebSocket room.
        - Emits "song_queue" and "currently_playing" events to the new user.
        - Emits an "active_users" event to all users in the same room.
    """
    # Create a SongScheduler instance for the room if it doesn't exist
    if room_id not in song_schedulers.keys():
        song_schedulers[room_id] = SongScheduler(room_id, socketio)
        song_schedulers[room_id].start_thread()
        active_users_by_room [room_id] = set()

    # Add the user's request.sid to the active users list for the room
    active_users_by_room[room_id].add(username)

    # Associate the user's socket ID with their username
    sid_to_user[request.sid] = username

    # Join the user to the WebSocket room
    join_room(room_id, request.sid)

    # Emit "song_queue" and "currently_playing" events to the new user
    emit("song_queue", {"queue": song_schedulers[room_id].get_queue()}, room=request.sid)
    emit("currently_playing", song_schedulers[room_id].get_current_song(), room=request.sid)

    # Emit an "active_users" event to all users in the same room
    emit("active_users", {"users": list(active_users_by_room[room_id])}, room=room_id)



@socketio.on("skip_song")
def handle_skip_song(room_id: int):
    """
    Handle "skip_song" event to skip the current song for all users in the specified room.

    Args:
        room_id (int): Room ID.

    Returns:
        None
    """
    song_schedulers[room_id].skip()

@socketio.on("pause_song")
def handle_pause_song(room_id: int):
    """
    Handle "pause_song" event to pause the current song for all users in the specified room.

    Args:
        room_id (int): Room ID.

    Returns:
        None
    """
    song_schedulers[room_id].pause()
    emit("pause_song","paused", room=room_id)

@socketio.on("play_song")
def handle_play_song(room_id: int):
    """
    Handle "play_song" event to play the current song for all users in the specified room.

    Args:
        room_id (int): Room ID.

    Returns:
        None
    """
    progress = song_schedulers[room_id].play()
    emit("play_song", {"progress":progress} ,room=room_id)


def add_to_queue(room_id: int, song_id: int):
    song_schedulers[room_id].add_to_queue(song_id)
    
"""
@socketio.on("control")
def handle_control(control: str):
    pass
@socketio.on("queue")
def handle_user_join(filename: str):
    pass

def play_next_song(room_id: int):
    emit("currently_playing", {"track": currently_playing, "progress": progress}, room=request.sid)
    pass

def update_queue(username, room_id):

    emit("song_queue", {"queue": get_queue(room_id)}, room=room_id)


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