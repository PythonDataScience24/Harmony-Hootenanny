import os
import subprocess
import sys
import time
from pytube import YouTube
from database import get_db_connection

class YoutubeDownloader:
    def __init__(self, output_path='./songs/'):
        self.output_path = output_path

    def download_video(self, youtube_link):
        try:
            yt = YouTube(youtube_link)
            # title, artist and duration work with or without the stream.
            title = yt.title
            artist = yt.author
            duration = yt.length
            src = f"{artist} - {title}.mp3"
            mp3_path = f"{self.output_path}{src}"
        
            # check if song exists
            with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT song_id FROM songs WHERE title=? AND artist=?", (title, artist))
                    existing_song = cursor.fetchone()
                    if existing_song:
                        print("FOUND")
                        return existing_song[0], 200  # returns songId
        except Exception as e:
                    print("Error: ", e)
                    return str(e), 500
        try:
            stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
            stream.download(output_path=self.output_path, filename=f"{title}.mp4")
            os.rename(f"{self.output_path}/{title}.mp4", mp3_path)
        except Exception as e:
            print("Pytube download failed! Using yt-dlp")
            max_retries = 10
            retry_delay = 1  # seconds
            while max_retries > 0:
                try:
                    yt_dlp_command = f"yt-dlp.exe -x --audio-format mp3 --audio-quality 0 {youtube_link} -o \"{mp3_path}\""
                    subprocess.check_call(yt_dlp_command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)
                    print("Download successful!")
                    break  # Exit the loop if successful
                except subprocess.CalledProcessError as e:
                    print(f"Download failed (retrying in {retry_delay} seconds): {e}")
                    max_retries -= 1
                    if max_retries > 0:
                        time.sleep(retry_delay)
            else:
                print(f"yt-dlp failed after {10} attempts")
                return "Couldn't download YouTube Video, try again", 500
        # File should be downloaded now
        with get_db_connection() as conn:
                # Put the song in the database and return the songId
                conn.cursor().execute("INSERT INTO songs (src, title, artist, duration) VALUES (?, ?, ?, ?)",
                                (src, title, artist, duration))
                conn.commit()
                song_id = conn.cursor().execute("SELECT song_id FROM songs ORDER BY song_id DESC LIMIT 1;").fetchone()
                return song_id[0], 200

        
        """
        

        Returns:
            _type_: _description_
            if stream:
                title = yt.title
                artist = yt.author
                duration = yt.length
                # Check if song is in the database already

                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT song_id FROM songs WHERE title=? AND artist=?", (title, artist))
                    existing_song = cursor.fetchone()
                    if existing_song:
                        print("FOUND")
                        return existing_song[0], 200  # returns songId

                    # Song doesn't exist, download it
                    mp3_path = f"{self.output_path}/{artist} - {title}.mp3"

                    stream.download(output_path=self.output_path, filename=f"{title}.mp4")
                    os.rename(f"{self.output_path}/{title}.mp4", mp3_path)
                    src = f"{artist} - {title}.mp3"
                    # Put the song in the database and return the songId
                    cursor.execute("INSERT INTO songs (src, title, artist, duration) VALUES (?, ?, ?, ?)",
                                   (src, title, artist, duration))
                    conn.commit()
                    return cursor.lastrowid, 200
            else:
                # Fallback: Use yt-dlp to get video information
                yt_dlp_command = f"yt-dlp --get-title --get-author --get-duration {youtube_link}"
                result = subprocess.run(yt_dlp_command, shell=True, capture_output=True, text=True)
                lines = result.stdout.strip().split("\n")
                title, artist, duration = lines
                src = f"{artist} - {title}.mp3"
                # Put the song in the database and return the songId
                cursor.execute("INSERT INTO songs (src, title, artist, duration) VALUES (?, ?, ?, ?)",
                               (src, title, artist, duration))
                conn.commit()
                return cursor.lastrowid, 200
        except Exception as e:
            print("Error: ", e)
            return str(e), 500

        """