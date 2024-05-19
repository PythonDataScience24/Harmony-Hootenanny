from pytube import YouTube
import os
from database import add_song_to_db, add_song_to_queue, get_db_connection

class YoutubeDownloader:
    def __init__(self, output_path='./songs/'):
        self.output_path = output_path

    def download_video(self, youtube_link, roomId, userId):
        try:
            yt = YouTube(youtube_link)
            stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
            if stream:
                # Creates filename and downloads the video
                mp3_path = f"{self.output_path}/{yt.title}.mp3"
                stream.download(output_path=self.output_path, filename=f"{yt.title}.mp4")
                # Renames the file, so it is in mp3 format
                os.rename(f"{self.output_path}/{yt.title}.mp4", mp3_path)
                
                # Adds the information into the database
                title = yt.title
                artist = yt.author
                duration = yt.length
                file_name = f"{yt.title}.mp3"
                
                # Insert song into the database
                add_song_to_db(title, artist, duration, file_name)

                # Fetch the song ID TODO (assuming the song ID is returned by add_song_to_db)
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM songs WHERE title = ? AND artist = ? AND duration = ? AND src = ?", (title, artist, duration, file_name))
                    song_id = cursor.fetchone()[0]

                # Add song to the queue
                add_song_to_queue(song_id, roomId, userId)

                return title, 200
            else:
                return 'No MP3 stream available for this video', 404
        except Exception as e:
            return str(e), 500
