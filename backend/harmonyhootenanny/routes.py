# Import necessary modules
import os
from flask import Blueprint, request, jsonify, send_from_directory
from pytube import YouTube

# Create a blueprint for your main routes
main = Blueprint("main", __name__)


# Endpoint to stream an mp3 file from the server
@main.route('/stream/mp3/<filename>')
def stream_mp3(filename):
    mp3_directory = './songs' # Path to the directory where MP3 files are stored
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
@main.route('/download',)
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