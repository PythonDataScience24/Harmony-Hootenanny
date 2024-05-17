from pytube import YouTube
import os

class YoutubeDownloader:
    def __init__(self, output_path='./songs/'):  # Geändertes Standardausgabeverzeichnis
        self.output_path = output_path

    def download_video(self, youtube_link):
        try:
            yt = YouTube(youtube_link)
            stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()  # Korrektur der Dateierweiterung
            if stream:
                # Erstellen des Dateinamens und Herunterladen des Streams
                mp3_path = f"{self.output_path}/{yt.title}.mp3"
                stream.download(output_path=self.output_path, filename=f"{yt.title}.mp4")  # Korrektur der Dateierweiterung
                # Umbenennen der heruntergeladenen Datei in .mp3
                os.rename(f"{self.output_path}/{yt.title}.mp4", mp3_path)
                return yt.title, 200  # Rückgabe des Dateinamens statt der gesamten Meldung
            else:
                return 'No MP3 stream available for this video', 404
        except Exception as e:
            return str(e), 505
