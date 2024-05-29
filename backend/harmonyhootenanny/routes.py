"""handles Rest-API of our backend"""
# Import necessary modules
import json
import os
import sqlite3
import re
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from harmonyhootenanny.events import add_to_scheduler_queue, get_or_create_scheduler
from database import add_song_to_db_queue, get_db_connection, get_user_id
from harmonyhootenanny.modules.youtubedownloader import YoutubeDownloader


# Create a blueprint for your main routes
main = Blueprint("main", __name__)


# Endpoint for signup
@main.route('/signup', methods=['POST'])
def signup():
    """
    Handle user signup requests.

    This endpoint allows users to create a new account by providing a username and password.
    It performs basic validation, checks for existing usernames, hashes the password, and
    stores the user information in the database.

    Request JSON format:
    {
        "username": "string",
        "password": "string",
        "confirm_password": "string"
    }

    Responses:
        201: User created successfully.
        {
            "message": "User created successfully",
            "username": "string"
        }
        400: Missing fields or passwords do not match.
        {
            "error": "Missing fields" | "Passwords do not match"
        }
        409: Username already exists.
        {
            "error": "Username already exists"
        }
        500: Database error.
        {
            "error": "Database error: <error_message>"
        }

    Returns:
        Response object with a JSON message and appropriate HTTP status code.
    """

    data = request.json
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')

    # Basic validation
    print(confirm_password, password)
    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    try:
        with get_db_connection() as db:
            cursor = db.cursor()
            # Check if the username already exists
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                return jsonify({"error": "Username already exists"}), 409

            # Hash password
            password_hash = generate_password_hash(password)

            # Save the user in the database
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",\
                           (username, password_hash))
            db.commit()
            return jsonify({"message": "User created successfully", "username": username}), 201

    except sqlite3.Error as e:
        # Handle database errors
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@main.route('/login', methods=['POST'])
def login():
    """
    Handle user login requests.

    This endpoint allows users to log in by providing a username and password.
    It performs basic validation, checks for existing usernames, verifies the password,
    and returns a success message if the credentials are correct.

    Request JSON format:
    {
        "username": "string",
        "password": "string"
    }

    Responses:
        200: Login successful.
        {
            "message": "Login successful",
            "username": "string"
        }
        400: Missing username or password.
        {
            "error": "Missing username or password"
        }
        404: User not found.
        {
            "error": "User not found"
        }
        401: Invalid password.
        {
            "error": "Invalid password"
        }
        500: Database error.
        {
            "error": "Database error: <error_message>"
        }

    Returns:
        Response object with a JSON message and appropriate HTTP status code.
    """

    # Receive user data
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Basic validation
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # Use the context manager to handle the database connection
    try:
        with get_db_connection() as db:
            cursor = db.cursor()
            # Check if the username exists in the database
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cursor.fetchone()

            if not user:
                return jsonify({"error": "User not found"}), 404

            # Verify password
            if check_password_hash(user['password_hash'], password):
                print(username,"successfully logged in")  # only for testing
                return jsonify({"message": "Login successful", "username": username}), 200
            print("Login failed due to invalid password")  # only for testing
            return jsonify({"error": "Invalid password"}), 401
    except sqlite3.Error as e:
        # Handle database errors
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# Only for Testing: Endpoint to list all users in db
@main.route('/users', methods=['GET'])
def list_users():
    """
    Handle requests to list all users.

    This endpoint retrieves all usernames from the database and returns them in a JSON response.

    Responses:
        200: Successfully retrieved the list of users.
        {
            "users": ["username1", "username2", ...]
        }
        500: Database error.
        {
            "error": "Database error: <error_message>"
        }

    Returns:
        Response object with a JSON message containing the list of 
        usernames and an appropriate HTTP status code.
    """
    try:
        with get_db_connection() as db:
            cursor = db.cursor()

            # Execute query to fetch all usernames
            cursor.execute("SELECT username FROM users")
            users = cursor.fetchall()

            # Extract usernames from the result
            user_list = [user['username'] for user in users]

            return jsonify({"users": user_list}), 200

    except sqlite3.Error as e:
        # Handle database errors
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@main.route('/stream/mp3/<filename>')
def stream_mp3(filename):
    """
    Stream an MP3 file.

    This endpoint streams an MP3 file from the server based on the given filename.
    The MP3 files are stored in the specified directory on the server.

    URL Parameters:
        filename (str): The name of the MP3 file to be streamed.

    Responses:
        200: Successfully streaming the requested MP3 file.
            The response contains the binary data of the MP3 file.
        404: File not found.
            {
                "error": "File not found"
            }

    Returns:
        Response object streaming the requested MP3 file.
    """
    mp3_directory = '../songs' # Path to the directory where MP3 files are stored
    return send_from_directory(mp3_directory, filename)

@main.route('/api/search', methods=['GET'])
def search_songs():
    """
    Search for songs based on a query string.

    This function handles GET requests to the '/api/search' endpoint. It retrieves song titles and artists 
    from the database that match the provided query string, constructs suggestions in the format 'title - artist',
    and returns them as JSON.

    Query Parameters:
        q (str): The search term used to find matching song titles. Defaults to an empty string if not provided.

    Responses:
        200: Successfully retrieved search suggestions.
            Returns a JSON object containing a list of suggestions, where each suggestion is in the format 'title - artist'.
        {
            "suggestions": [
                {"title": "Song Title - Artist"},
                {"title": "Another Title - Another Artist"},
                ...
            ]
        }
        500: Database error.
            Returns a JSON object with an error message if there is an issue with the database connection or query execution.
        {
            "error": "Database error: <error_message>"
        }

    Returns:
        Response object with a JSON message containing a list of search suggestions and an appropriate HTTP status code.
    """
    query = request.args.get('q', '')
    suggestions = []

    try:
        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT title, artist FROM songs WHERE title LIKE ?", ('%' + query + '%',))
            results = cursor.fetchall()
            
            for row in results:
                suggestions.append({'title': f"{row['title']} - {row['artist']}"})

    except sqlite3.Error as e:
        return jsonify({'error': f"Database error: {str(e)}"}), 500

    return jsonify({'suggestions': suggestions})

@main.route('/api/download/youtube', methods=['POST'])
def searchbar():
    """
    Search for a YouTube song and add it to the queue if found.

    This function handles POST requests to the '/api/download/youtube' endpoint. It receives a JSON object
    containing a search value (YouTube link or song title), extracts the room ID and user ID from the user data,
    checks if the search value is a valid YouTube link, and downloads the video if so. If the search value is not
    a YouTube link, it returns a message indicating that. If the video is successfully downloaded, it adds the song
    to the queue and returns a success message.

    Request JSON format:
    {
        "searchvalue": "string",
        "userData": {
            "room_Id": "int",
            "user_Id": "int"
        }
    }

    Responses:
        200: Successfully found and added the YouTube song to the queue.
            Returns a JSON object with a success message and the title of the downloaded song.
        {
            "message": "Youtube song successfully found",
            "title": "string"
        }
        404: Failed to download the video.
            Returns a JSON object with an error message.
        {
            "error": "Failed to download video"
        }

    Returns:
        Response object with a JSON message and an appropriate HTTP status code.
    """
    data = request.json
    search_value = data.get('searchvalue')
    print("Link: ",search_value)
    userdata = data.get('userData')
    username=userdata['username']

    room_id = data.get('roomId')
    user_id = get_user_id(username)

    # Check if it is a Youtube link
    youtube_regex = r'^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$'
    
    if re.match(youtube_regex, search_value):
        # Initialize the YoutubeDownloader only, if it is a Youtube link
        youtube_downloader = YoutubeDownloader()
        song_id, status_code = youtube_downloader.download_video(search_value)
        if status_code == 200:
            # Ensure the scheduler is initialized
            get_or_create_scheduler(room_id)
            # Add the song to the queue in songSchedular
            add_to_scheduler_queue(room_id, song_id)
            # Add Song to queue in database
            add_song_to_db_queue(song_id, room_id, user_id)
            return jsonify({'message': 'Youtube song successfully found'}), 200
        return jsonify({'error': 'Failed to download video'}), status_code
    else:
        # Return a message indicating that it was not a YouTube link
        return jsonify({'message': 'Not a YouTube link'}), 200

@main.route('/api/selected-song', methods=['POST'])
def handle_selected_song():
    """
    Handle a selected song and add it to the queue if found in the database.

    This function handles POST requests to the '/api/selected-song' endpoint. It receives a JSON object
    containing the selected song title, extracts the room ID and user ID from the user data, splits the
    title into title and artist, and searches the database for a matching song. If the song is found, it
    adds it to the queue and returns a success message with the song ID. If the song is not found or the
    input is invalid, it returns an error message.

    Request JSON format:
    {
        "selectedSong": "string",
        "userData": {
            "room_Id": "int",
            "user_Id": "int"
        }
    }

    Responses:
        200: Successfully found and added the selected song to the queue.
            Returns a JSON object with a success message and the ID of the found song.
        {
            "message": "Selected song found and added to queue",
            "songId": "int"
        }
        404: Song not found in the database.
            Returns a JSON object with an error message.
        {
            "error": "Song not found"
        }
        400: Invalid input or format of the selected song.
            Returns a JSON object with an error message.
        {
            "error": "Invalid input" | "Invalid format of selected song"
        }

    Returns:
        Response object with a JSON message and an appropriate HTTP status code.
    """
    data = request.json
    selected_song = data.get('selectedSong')
    userdata = data.get('userData')
    username=userdata['username']

    room_id = data.get('roomId')
    user_id = get_user_id(username)

    if selected_song:
        try:
            # Split the selected song into title and artist
            title, artist = selected_song.rsplit(' - ', 1)
            with get_db_connection() as db:
                cursor = db.cursor()
                cursor.execute("SELECT song_id FROM songs WHERE title = ? AND artist = ?", (title, artist))
                result = cursor.fetchone()

                if result:
                    song_id = result['song_id']
                   # Ensure the scheduler is initialized
                    get_or_create_scheduler(room_id)
                    # Add the song to the queue in songSchedular
                    add_to_scheduler_queue(room_id, song_id)
                    # Add Song to queue in database
                    add_song_to_db_queue(song_id, room_id, user_id)
                    return jsonify({'message': 'Selected song found and added to queue', 'songId': song_id}), 200
                else:
                    return jsonify({'error': 'Song not found'}), 404

        except sqlite3.Error as e:
            return jsonify({'error': f"Database error: {str(e)}"}), 500
        except ValueError:
            return jsonify({'error': 'Invalid format of selected song'}), 400

    else:
        return jsonify({'error': 'Invalid input'}), 400

#  Creates three rooms in the database if they don't exist already.
def create_rooms():
    """
    Create predefined rooms in the database if they don't exist.
    This function connects to the database, checks if the rooms with ids 1, 2, and 3 exist,
    and if they don't, it creates them. This function is called when the application starts.
    """
    room_ids = [1, 2, 3]

    with get_db_connection() as conn:
        cursor = conn.cursor()

        for room_id in room_ids:
            cursor.execute("SELECT * FROM rooms WHERE room_id = ?", (room_id,))
            result = cursor.fetchone()
            if not result:
                cursor.execute("INSERT INTO rooms (room_id) VALUES (?)", (room_id,))

        conn.commit()

# Call the function when the application starts
create_rooms()

# Endpoint to get the dashboard data
@main.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """
    - This functions connects to the database and retrieves the top 3 artists for each room.
    - It returns the data in JSON format.
    
    """
    try:
        def get_stats(cursor, query, room_id):
            cursor.execute(query, (room_id,))
            rows = cursor.fetchall()
            return [{description[0]: value for description, value in zip(cursor.description, row)} for row in rows]

    
        with get_db_connection() as db:
            cursor = db.cursor()
            room_data = {}
            for room_id in [1, 2, 3]:
                 room_data[f'room{room_id}'] ={
    
                    'top_artist': get_stats(cursor, """
                               SELECT artist, COUNT(*) as count
                                FROM songs JOIN queues on songs.song_id = queues.song_id
                                WHERE queues.room_id=?
                                GROUP BY artist
                                ORDER BY count DESC
                                Limit 3
                                """, room_id),
                     
                }

        return jsonify(room_data), 200
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500