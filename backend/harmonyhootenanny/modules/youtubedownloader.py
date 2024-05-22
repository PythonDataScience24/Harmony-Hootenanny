from pytube import YouTube
import os
from database import get_db_connection

class YoutubeDownloader:
    def __init__(self, output_path='./songs/'):
        self.output_path = output_path

    def download_video(self, youtube_link):
        try:
            yt = YouTube(youtube_link)
            stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
            if stream:
                title = yt.title
                artist = yt.author
                duration = yt.length
                # Check if song is in database already
                
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT song_id FROM songs WHERE title=? AND artist=?", (title, artist))
                    existing_song = cursor.fetchone()
                    if existing_song:
                        print("FOUND")
                        return existing_song[0], 200  # returns songId
                
                    # Song doenst exist, download it
                    mp3_path = f"{self.output_path}/{artist} - {title}.mp3"
                    stream.download(output_path=self.output_path, filename=f"{title}.mp4")
                    os.rename(f"{self.output_path}/{title}.mp4", mp3_path)
                    src = f"{artist} - {title}.mp3"
                    # Put the song in the database and return the songId
                    cursor.execute("INSERT INTO songs (src, title, artist, duration) VALUES (?, ?, ?, ?)", (src, title, artist, duration))
                    conn.commit()
                    return cursor.lastrowid , 200
                
            else:
                return 'No MP3 stream available for this video', 404
        except Exception as e:
            print("Error: ", e)
            return str(e), 500
