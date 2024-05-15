from pytube import YouTube

class YoutubeDownloader:
    def __init__(self, output_path='./songs/'):
        self.output_path = output_path

    def download_video(self, youtube_link):
        try:
            yt = YouTube(youtube_link)
            stream = yt.streams.filter(only_audio=True, file_extension='mp3').first()
            if stream:
                stream.download(output_path=self.output_path)
                return 'Video downloaded successfully', 200
            else:
                return 'No MP3 stream available for this video', 400
        except Exception as e:
            return str(e), 500