from .extensions import socketio
from flask_socketio import emit
from flask import request

# Initialize an empty dictionary to store active users in each room
active_users_by_room = {}

@socketio.on("connect")
def handle_connect():
    print("client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("client disconnected")
 # Remove the user's request.sid from the active users list when they disconnect
    for room_id, users in active_users_by_room.items():
        if request.sid in users:
            users.remove(request.sid)
            emit("active_users", {"users": list(users)}, room=room_id)

@socketio.on("join_room")
def handle_join_room(room_id: int, username: str):
    # Add the user to the room in the database (if needed)
    # Example: UserRoom.create(user_id=user_id, room_id=room_id)

    # Add the user's request.sid to the active users list for the room
    if room_id not in active_users_by_room:
        active_users_by_room[room_id] = set()
    active_users_by_room[room_id].add(request.sid)

    # Emit "active_users" event to all users in the same room
    emit("active_users", {"users": list(active_users_by_room[room_id])}, room=room_id)

    # Emit "song_queue" and "currently_playing" events to the new user
    song_queue = get_song_queue_for_user(room_id)  # Implement this function
    currently_playing = get_currently_playing_track(room_id)  # Implement this function
    emit("song_queue", {"queue": song_queue}, room=request.sid)
    emit("currently_playing", {"track": currently_playing}, room=request.sid)

    pass





@socketio.on("control")
def handle_control(control: str):
    pass
@socketio.on("queue")
def handle_user_join(filename: str):
    pass







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