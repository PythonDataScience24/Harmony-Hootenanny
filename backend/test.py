from pytube import YouTube
import subprocess
import sys

"""_summary_
def execute(command):
    subprocess.check_call(command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)

youtube_link = "https://www.youtube.com/watch?v=gloB2gwVVsk"
yt = YouTube(youtube_link)
title = yt.title
artist = yt.author
duration = yt.length
try:
    stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
    stream.download(output_path=self.output_path, filename=f"{title}.mp4")
except Exception as e:
    print("Pytube failed! Using yt-dlp")
    # Fallback: Use yt-dlp to get video information
    # ./yt-dlp.exe -x --audio-format mp3 --audio-quality 0 https://www.youtube.com/watch?v=s9gRg3_A-RM
    # ./yt-dlp.exe -x --audio-format mp3 --audio-quality 0 https://www.youtube.com/watch?v=s9gRg3_A-RM
    yt_dlp_command = f"./yt-dlp.exe -x --audio-format mp3 --audio-quality 0 {youtube_link}"
    cmd = "dir"
    execute(yt_dlp_command)
finally:
    print("downloaded")
"""
import time
output_path='./songs/'
def download_with_retry(youtube_link):
    max_retries = 10
    retry_delay = 1  # seconds
    while max_retries > 0:
        try:
            yt_dlp_command = f"yt-dlp.exe -x --audio-format mp3 --audio-quality 0 {youtube_link} -o {output_path}test123.mp3"
            subprocess.check_call(yt_dlp_command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)
            print("Download successful!")
            break  # Exit the loop if successful
        except subprocess.CalledProcessError as e:
            print(f"Download failed (retrying in {retry_delay} seconds): {e}")
            max_retries -= 1
            if max_retries > 0:
                time.sleep(retry_delay)
    else:
        print("Max retries reached. Download failed.")

# Example usage
youtube_link = "https://www.youtube.com/watch?v=gloB2gwVVsk"
download_with_retry(youtube_link)