from database import get_current_song, get_queue
from .extensions import socketio
from flask_socketio import emit, join_room, leave_room
from flask import request

# Initialize an empty dictionary to store active users in each room
active_users_by_room = {}
sid_to_user = {}
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

    emit("active_users", {"users":list(active_users_by_room[room_id])}, room=key)

@socketio.on("join_room")
def handle_join_room(room_id: int, username: str):
    # Add the user to the room in the database (if needed)
    # Example: UserRoom.create(user_id=user_id, room_id=room_id)

    sid_to_user[request.sid] = username


    join_room(room_id, request.sid)
    # Add the user's request.sid to the active users list for the room
    if room_id not in active_users_by_room:
        active_users_by_room[room_id] = set()
    active_users_by_room[room_id].add(username)

    print(active_users_by_room)
    print(sid_to_user)
    # Emit "active_users" event to all users in the same room
    emit("active_users", {"users": list(active_users_by_room[room_id])}, to=room_id)

    # Emit "song_queue" and "currently_playing" events to the new user
    
    # get_song_queue_for_user(room_id)  # Implement this function
    currently_playing = "Men At Work - Down Under (Official HD Video).mp3"# get_currently_playing_track(room_id)  # Implement this function
    print(active_users_by_room[room_id])


    emit("song_queue", {"queue": get_queue(room_id)}, room=request.sid)


    emit("currently_playing", get_current_song(room_id), room=request.sid)


    emit("active_users", {"users":list(active_users_by_room[room_id])}, room=room_id)

    pass





@socketio.on("control")
def handle_control(control: str):
    pass
@socketio.on("queue")
def handle_user_join(filename: str):
    pass

def next_song():
    #emit("currently_playing", {"track": currently_playing, "progress": progress}, room=request.sid)
    pass


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