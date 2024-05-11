from flask import Flask, request, jsonify, send_from_directory, g
from flask_socketio import SocketIO,emit
from flask_cors import CORS
import os
import sqlite3
from sqlite3 import Error
from pytube import YouTube

app = Flask(__name__)

CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")

# Connect to database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        try:
            db = g._database = sqlite3.connect("database.db")
            print("Successfully connected to database")
            return db
        except Error as e:
            print(f"Failed to connect to the database: {e}")
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

# Open new db connection before processing a request
@app.before_request
def before_request():
    g.db = get_db()

# Close db connection after request has been served
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET'])
def home():
    return "Hello, Flask!"

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

""" Websocket code """

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