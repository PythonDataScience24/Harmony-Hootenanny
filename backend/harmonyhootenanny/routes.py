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
    

