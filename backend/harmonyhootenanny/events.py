import re
from harmonyhootenanny.modules.youtubedownloader import YoutubeDownloader
from harmonyhootenanny.modules.SongScheduler import SongScheduler
from database import add_user_action, get_current_song, get_queue, get_song_id_by_name
from .extensions import socketio
from flask_socketio import emit, join_room, leave_room
from flask import jsonify, request

# Initialize an empty dictionary to store active users in each room
active_users_by_room = {}  # {room_id: {username1, username2, ...}}
sid_to_user = {}  # {socket_id: username}
song_schedulers: dict[int, SongScheduler] = {}  # {room_id: SongScheduler instance}

def get_or_create_scheduler(room_id):
    """
    Retrieves the SongScheduler instance for a given room_id, or creates one if it does not exist.

    Args:
        room_id (int): The unique identifier for the room.

    Returns:
        SongScheduler: The SongScheduler instance associated with the specified room_id.

    This function checks if a SongScheduler instance exists for the provided room_id in the
    song_schedulers dictionary. If an instance does not exist, it creates a new SongScheduler
    for that room, starts its scheduling thread, and stores it in the song_schedulers dictionary.
    Finally, it returns the SongScheduler instance for the specified room_id.
    """
    if room_id not in song_schedulers:
        song_schedulers[room_id] = SongScheduler(room_id, socketio)
        song_schedulers[room_id].start_thread()
    return song_schedulers[room_id]

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

    # Add user action to database
    username = sid_to_user[request.sid]
    add_user_action('leave_room', room_id, username)

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
    scheduler = get_or_create_scheduler(room_id)

    # Add the user's request.sid to the active users list for the room
    active_users_by_room.setdefault(room_id, set()).add(username)

    # Associate the user's socket ID with their username
    sid_to_user[request.sid] = username

    # Join the user to the WebSocket room
    join_room(room_id, request.sid)

    # Add user action to database
    add_user_action('join_room', room_id, username)

    # Emit "song_queue" and "currently_playing" events to the new user
    emit("song_queue", {"queue": scheduler.get_queue()}, room=request.sid)
    emit("currently_playing", scheduler.get_current_song(), room=request.sid)

    # Emit an "active_users" event to all users in the same room
    emit("active_users", {"users": list(active_users_by_room[room_id])}, room=room_id)



@socketio.on("skip_song")
def handle_skip_song(room_id: int, username: str):
    """
    Handle "skip_song" event to skip the current song for all users in the specified room.

    Args:
        room_id (int): Room ID.

    Returns:
        None
    """
    scheduler = get_or_create_scheduler(room_id)
    scheduler.skip()
    
    # Add user action to database
    add_user_action('skip_song', room_id, username)

@socketio.on("pause_song")
def handle_pause_song(room_id: int):
    """
    Handle "pause_song" event to pause the current song for all users in the specified room.

    Args:
        room_id (int): Room ID.

    Returns:
        None
    """
    scheduler = get_or_create_scheduler(room_id)
    scheduler.pause()
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
    scheduler = get_or_create_scheduler(room_id)
    progress = scheduler.play()
    emit("play_song", {"progress":progress} ,room=room_id)


@socketio.on("select_song")
def handle_select_song(song_title_selected:str, room_id: int):
    res = song_title_selected.split(" - ")
    title, artist = res[0], res[1]
    song_id = get_song_id_by_name(title)
    add_to_scheduler_queue(room_id, song_id)

@socketio.on("download_song")
def handle_download_song(url:str, room_id: int):
    print(url, room_id)
    # Check if it is a Youtube link
    youtube_regex = r'^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$'
    if re.match(youtube_regex, url):
        # Initialize the YoutubeDownloader only, if it is a Youtube link
        youtube_downloader = YoutubeDownloader()
        song_id, status_code = youtube_downloader.download_video(url)
        if status_code == 200:
            add_to_scheduler_queue(room_id, song_id)
        else:
            print("Download failed!")
    else:
        # Return a message indicating that it was not a YouTube link
        print("URL was not a valid YouTube link")




def add_to_scheduler_queue(room_id: int, song_id: int):
    scheduler = get_or_create_scheduler(room_id)
    scheduler.add_to_queue(song_id)
    emit("song_queue", {"queue": scheduler.get_queue()}, room=room_id)
    
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