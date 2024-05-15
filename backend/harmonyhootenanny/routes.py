# Import necessary modules
import os
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from pytube import YouTube
from database import get_db_connection


# Create a blueprint for your main routes
main = Blueprint("main", __name__)


# Endpoint for signup
@main.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    confirmPassword = data.get('confirmPassword')

    # Basic validation
    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400
    
    if password != confirmPassword:
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
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            db.commit()

            return jsonify({"message": "User created successfully", "username": username}), 201

    except sqlite3.Error as e:
        # Handle database errors
        return jsonify({"error": "Database error: {}".format(str(e))}), 500


# Endpioint for login and signup
@main.route('/login', methods=['POST'])
def login():
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
            else:
                print("Login failed due to invalid password")  # only for testing
                return jsonify({"error": "Invalid password"}), 401
    except sqlite3.Error as e:
        # Handle database errors
        return jsonify({"error": "Database error: {}".format(str(e))}), 500

# Only for Testing: Endpoint to list all users in db
@main.route('/users', methods=['GET'])
def list_users():
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
        return jsonify({"error": "Database error: {}".format(str(e))}), 500

# Endpoint to stream an mp3 file from the server
@main.route('/stream/mp3/<filename>')
def stream_mp3(filename):
    mp3_directory = '../songs' # Path to the directory where MP3 files are stored
    return send_from_directory(mp3_directory, filename)

# Search endpoint that looks for files matching the query in the song directory
@main.route('/api/search', methods=['GET'])
def search_songs():
    query = request.args.get('q', '')  # Retrieve search term from the query string; default to empty string if not provided
    mp3_directory = './songs/'
    suggestions = []
     # Iterate over all files in the directory and check if their name contains the search term
    for filename in os.listdir(mp3_directory):
        if query.lower() in filename.lower() and filename.endswith('.mp3'):
            suggestions.append({'title': filename})
    # Return the list of suggestions as a JSON response
    return jsonify({'suggestions': suggestions})

# download endpoint
@main.route('/api/download/youtube', methods=['POST'])
def download_youtube():
    youtube_link = request.json.get('youtube_link')
    if not youtube_link:
        return jsonify({'error': 'No YouTube link provided'}), 400

    try:
        mp3_path = download_youtube_mp3(youtube_link)
        if mp3_path:
            return jsonify({'message': 'Video downloaded successfully', 'mp3_path': mp3_path}), 200
        else:
            return jsonify({'error': 'Failed to download video'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def download_youtube_mp3(youtube_link):
    output_directory = './songs'
    
    try:
        # Create YouTube video object
        yt = YouTube(youtube_link)
        
        # Select MP3 stream (if available)
        stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        
        if stream:
            # Download and save MP3
            mp3_path = os.path.join(output_directory, f"{yt.title}.mp3")
            stream.download(output_path=output_directory, filename=f"{yt.title}.mp3")  # Set filename to desired value
            print(f"Success downloading YouTube video")
            return mp3_path  # Return path to downloaded MP3 file
        else:
            print(f"No success downloading YouTube video, as no MP3 download available")
            return None  # Return None if no MP3 stream available
    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
        return None
    

