# Import necessary modules
import os
from flask import Blueprint, request, jsonify

# Create a blueprint for your main routes
main = Blueprint("main", __name__)

# Define the search endpoint
@main.route("/api/search", methods=["GET"])
def search_songs():
    # Retrieve the search term from the query string; default to an empty string if not provided
    query = request.args.get("q", "")
    
    # Specify the directory where your MP3 files are stored
    mp3_directory = "./songs/"
    
    # Initialize an empty list to store suggestions
    suggestions = []
    
    # Iterate over all files in the directory and check if their name contains the search term
    for filename in os.listdir(mp3_directory):
        if query.lower() in filename.lower() and filename.endswith(".mp3"):
            suggestions.append({"title": filename})
    
    # Return the list of suggestions as a JSON response
    return jsonify({"suggestions": suggestions})

