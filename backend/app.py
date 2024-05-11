from flask import Flask, request, jsonify, send_from_directory, g
from flask_socketio import SocketIO,emit
from flask_cors import CORS
import os
import sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash, check_password_hash
from pytube import YouTube

app = Flask(__name__)

CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")


# Connect to database
def get_db():
    try:
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect("database.db")
            db.row_factory = sqlite3.Row
            print("Successfully connected to database")
        return db
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return None
        
# Initialize db using the SQL schema from "schema.sql" file
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            # Execute schema to create the specified tables
            db.cursor().executescript(f.read())
        db.commit()
        db.close() # Ensures the database connection is closed after the schema is applied

# Close db connection after request has been served
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET'])
def home():
    return "Hello, Flask!"

# Endpoint for signup
@app.route('/signup', methods=['POST'])
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
        # Check if username already exists
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"error": "Username already exists"}), 409

        # Hash password
        password_hash = generate_password_hash(password)

        # Save the user in the database
        db = get_db()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        db.commit()

        return jsonify({"message": "User created successfully", "username": username}), 201
    except sqlite3.Error as e:
        # Handle database errors
        return jsonify({"error": "Database error: {}".format(str(e))}), 500
    finally:
        # Close the cursor after execution
        cursor.close()


# Endpioint for login and signup
@app.route('/login', methods=['POST'])
def login():
    # Receive user data
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Basic validation
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    
    try:
        # Get database connection
        db = get_db()
        cursor = db.cursor()

        # Check if the username exists in the database
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Verify password
        if check_password_hash(user['password_hash'], password):
            print(username,"successfully logged in") # only for testing
            return jsonify({"message": "Login successful", "username": username}), 200
        else:
            print("Login failed due to invalid password") # only for testing
            return jsonify({"error": "Invalid password"}), 401
    except sqlite3.Error as e:
        # Handle database errors
        return jsonify({"error": "Database error: {}".format(str(e))}), 500
    finally:
        # Close the cursor after execution
        cursor.close()

# Only for Testing: Endpoint to list all users in db
@app.route('/users', methods=['GET'])
def list_users():
    try:
        # Get database connection
        db = get_db()
        cursor = db.cursor()

        # Execute query to fetch all users
        cursor.execute("SELECT username FROM users")
        users = cursor.fetchall()

        # Extract usernames from the result
        user_list = [user['username'] for user in users]

        return jsonify({"users": user_list}), 200
    except sqlite3.Error as e:
        # Handle database errors
        return jsonify({"error": "Database error: {}".format(str(e))}), 500
    finally:
        # Close the cursor after execution
        cursor.close()

# Endpoint to stream an mp3 file from the server
@app.route('/stream/mp3/<filename>')
def stream_mp3(filename):
    mp3_directory = './songs' # Path to the directory where MP3 files are stored
    return send_from_directory(mp3_directory, filename)

# Search endpoint that looks for files matching the query in the song directory
@app.route('/api/search', methods=['GET'])
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

@app.route('/api/greet', methods=['GET'])
def greet():
    response = {"message": "Hello from Flask!"}
    return jsonify(response)


@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data':'This text was fetched using an HTTP call to server on render'}
    return jsonify(data)

@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect",{"data":f"id: {request.sid} is connected"})

@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ",str(data))
    emit("data",{'data':data,'id':request.sid},broadcast=True)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)

@app.route('/download',)
def download_youtube_video():
    youtube_link = request.json.get('youtube_link')
    if not youtube_link:
        return 'No YouTube link provided', 400
    try:
        yt = YouTube(youtube_link)
        stream = yt.streams.filter(only_audio=True, file_extension='mp3').first()
        if stream:
            stream.download(output_path='./songs/')
            return 'Video downloaded successfully', 200
        else:
            return 'No MP3 stream available for this video', 400
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)