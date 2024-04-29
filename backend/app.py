from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO,emit
from flask_cors import CORS
import os

app = Flask(__name__)


CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")



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
    mp3_directory = './backend/songs/'
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


if __name__ == '__main__':
    app.run(debug=True)
