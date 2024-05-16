"""handles Rest-API of our backend"""
# Import necessary modules
import os
import sqlite3
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
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
    Search for MP3 files based on a query.

    This endpoint allows users to search for MP3 files in the server's song directory.
    It returns a list of file names that contain the search term.

    Query Parameters:
        q (str): The search term used to find matching MP3 files. 
        Defaults to an empty string if not provided.

    Responses:
        200: Successfully retrieved search suggestions.
        {
            "suggestions": [
                {"title": "filename1.mp3"},
                {"title": "filename2.mp3"},
                ...
            ]
        }

    Returns:
        Response object with a JSON message containing a list of matching MP3 file names.
    """
    query = request.args.get('q', '')
    # Retrieve search term from the query string; default to empty string if not provided
    mp3_directory = './songs/'
    suggestions = []
     # Iterate over all files in the directory and check if their name contains the search term
    for filename in os.listdir(mp3_directory):
        if query.lower() in filename.lower() and filename.endswith('.mp3'):
            suggestions.append({'title': filename})
    # Return the list of suggestions as a JSON response
    return jsonify({'suggestions': suggestions})

@main.route('/api/download/youtube', methods=['POST'])
def download_youtube():
    """
    Download a YouTube video as an MP3.

    This endpoint allows users to download the audio of a YouTube video as an MP3 file.
    The YouTube link is provided in the request body.

    Request JSON format:
    {
        "youtube_link": "string"
    }

    Responses:
        200: Video downloaded successfully.
        {
            "message": "Video downloaded successfully",
            "mp3_path": "path/to/downloaded/file.mp3"
        }
        400: No YouTube link provided.
        {
            "error": "No YouTube link provided"
        }
        500: Failed to download video or other errors.
        {
            "error": "Failed to download video" | "<error_message>"
        }

    Returns:
        Response object with a JSON message and appropriate HTTP status code.
    """
    youtube_link = request.json.get('youtube_link')
    if not youtube_link:
        return jsonify({'error': 'No YouTube link provided'}), 400

    # Initialize the YoutubeDownloader
    youtube_downloader = YoutubeDownloader()
    mp3_path = youtube_downloader.download_video(youtube_link)
    if mp3_path[1]==200:
        return jsonify({'message': 'Video downloaded successfully', 'mp3_path': mp3_path}), 200
    return jsonify({'error': 'Failed to download video'}), 500

def create_rooms():
    """Create predefined rooms in the database if they don't exist."""
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