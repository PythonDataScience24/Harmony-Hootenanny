from pytube import YouTube
import os
from harmonyhootenanny.events import add_to_queue
from database import add_song_to_db, add_song_to_queue, get_db_connection

class YoutubeDownloader:
    def __init__(self, output_path='./songs/'):
        self.output_path = output_path

    def download_video(self, youtube_link, roomId, userId):
        try:
            yt = YouTube(youtube_link)
            stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
            if stream:
                title = yt.title
                artist = yt.author
                duration = yt.length
                file_name = f"{yt.title}.mp3"

                # Check if the song already exists in the database
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM songs WHERE title = ?", (title,))
                    existing_song = cursor.fetchone()

                if existing_song:
                    # Song already exists, do not download again
                    song_id = existing_song[0]
                else:
                    # Song does not exist, download it
                    mp3_path = f"{self.output_path}/{yt.title}.mp3"
                    stream.download(output_path=self.output_path, filename=f"{yt.title}.mp4")
                    os.rename(f"{self.output_path}/{yt.title}.mp4", mp3_path)

                    # Insert song into the database
                    add_song_to_db(title, artist, duration, file_name)

                    # Fetch the song ID
                    with get_db_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT id FROM songs WHERE title = ? AND artist = ? AND duration = ? AND src = ?", (title, artist, duration, file_name))
                        song_id = cursor.fetchone()[0]

                # Add song to the queue
                add_to_queue(roomId, song_id)
                add_song_to_queue(song_id, roomId, userId)

                return title, 200
            else:
                return 'No MP3 stream available for this video', 404
        except Exception as e:
            return str(e), 500
