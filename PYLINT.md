# Pylinting

## routes.py

### Pylint Output before fixing:

\*\*\*\*\*\*\*\*\*\*\*\*\* Module harmonyhootenanny.routes
==routes.py:25:0: C0303: Trailing whitespace (trailing-whitespace)==
==routes.py:42:0: C0301: Line too long (114/100) (line-too-long)==
==routes.py:63:0: C0303: Trailing whitespace (trailing-whitespace)==
==routes.py:115:0: C0301: Line too long (124/100) (line-too-long)==
==routes.py:140:0: C0303: Trailing whitespace (trailing-whitespace)==
==routes.py:144:0: C0303: Trailing whitespace (trailing-whitespace)==
==routes.py:148:0: C0303: Trailing whitespace (trailing-whitespace)==
==routes.py:151:0: C0303: Trailing whitespace (trailing-whitespace)==
==routes.py:155:0: C0301: Line too long (118/100) (line-too-long)==
==routes.py:164:0: C0303: Trailing whitespace (trailing-whitespace)==
==routes.py:165:0: C0305: Trailing newlines (trailing-newlines)==
==routes.py:1:0: C0114: Missing module docstring (missing-module-docstring)==
==routes.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)==
==routes.py:20:4: C0103: Variable name "confirmPassword" doesn't conform to snake_case naming style (invalid-name)==
==routes.py:49:33: C0209: Formatting a regular string which could be an f-string (consider-using-f-string)==
==routes.py:54:0: C0116: Missing function or method docstring (missing-function-docstring)==
==routes.py:76:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)==
==routes.py:84:33: C0209: Formatting a regular string which could be an f-string (consider-using-f-string)==
==routes.py:88:0: C0116: Missing function or method docstring (missing-function-docstring)==
==routes.py:104:33: C0209: Formatting a regular string which could be an f-string (consider-using-f-string)==
==routes.py:108:0: C0116: Missing function or method docstring (missing-function-docstring)==
==routes.py:114:0: C0116: Missing function or method docstring (missing-function-docstring)==
==routes.py:127:0: C0116: Missing function or method docstring (missing-function-docstring)==
==routes.py:138:11: W0718: Catching too general exception Exception (broad-exception-caught)==
==routes.py:134:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)==
==routes.py:142:0: C0116: Missing function or method docstring (missing-function-docstring)==
==routes.py:161:11: W0718: Catching too general exception Exception (broad-exception-caught)==
==routes.py:152:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)==
==routes.py:156:18: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)==
==routes.py:159:18: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)==
==routes.py:5:0: C0411: standard import "sqlite3" should be placed before third party imports "flask.Blueprint", "werkzeug.security.generate_password_hash" (wrong-import-order)==

---

Your code has been rated at 6.77/10

### New Code:

```
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
```
