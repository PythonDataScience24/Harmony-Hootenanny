
from harmonyhootenanny.modules.SongScheduler import SongScheduler
from database import get_current_song, get_queue
from .extensions import socketio
from flask_socketio import emit, join_room, leave_room
from flask import request

# Initialize an empty dictionary to store active users in each room
active_users_by_room = {}
sid_to_user = {}
song_schedulers: dict[int, SongScheduler] = {}

@socketio.on("connect")
def handle_connect():
    print("client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("client disconnected")
    room_id = 0
    print(active_users_by_room, sid_to_user)
    username_left = sid_to_user[request.sid]
    for key, menge in active_users_by_room.items():
        for username in menge:
            if username_left == username:
                room_id = key 
    active_users_by_room[key].remove(username_left)
    del sid_to_user[request.sid]

    print(active_users_by_room, sid_to_user)

    leave_room(key, request.sid)
    handle_play_song(room_id)

    emit("active_users", {"users":list(active_users_by_room[room_id])}, room=key)
    print("Emitted active users and played song")


@socketio.on("join_room")
def handle_join_room(room_id: int, username: str):
    # TODO when user joins different room, remove from old room
    # TODO room 1 bug doesn't display left members

    if room_id not in song_schedulers.keys():
        # Song Scheduler creation
        song_schedulers[room_id] = SongScheduler(room_id, socketio)
        song_schedulers[room_id].start_thread()
        # create list of active users
        active_users_by_room[room_id] = set()      

    # Add the user's request.sid to the active users list for the room
    active_users_by_room[room_id].add(username)
    # Create a link between sid's and usernames
    sid_to_user[request.sid] = username

    # Add user to websocket room
    join_room(room_id, request.sid)     

    # Emit "song_queue" and "currently_playing" events to the new user
    emit("song_queue", {"queue": song_schedulers[room_id].get_queue()}, room=request.sid)
    emit("currently_playing", song_schedulers[room_id].get_current_song(), room=request.sid)

    # Emit "active_users" event to all users in the same room
    emit("active_users", {"users":list(active_users_by_room[room_id])}, room=room_id)


@socketio.on("skip_song")
def handle_skip_song(room_id: int):
    song_schedulers[room_id].skip()

@socketio.on("pause_song")
def handle_pause_song(room_id: int):
    song_schedulers[room_id].pause()
    emit("pause_song","paused", room=room_id)

@socketio.on("play_song")
def handle_play_song(room_id: int):
    progress = song_schedulers[room_id].play()
    emit("play_song", {"progress":progress} ,room=room_id)



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