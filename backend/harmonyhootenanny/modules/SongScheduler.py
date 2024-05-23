

import threading
import time
from ..extensions import socketio
from flask_socketio import emit
from database import get_song_by_id, get_queue

class _Song:
    """
    A private class for managing queues and current songs.

    Attributes:
        src (str): The source of the song (.mp3 file).
        title (str): The title of the song.
        artist (str): The artist or performer of the song.
        duration (int): The duration of the song in seconds.

    Methods:
        dictify() -> dict:
            Returns a dictionary representation of the song with keys:
                - "title": The song title.
                - "artist": The artist's name.
                - "filename": The source (file path or URL).
                - "duration": The song duration in seconds.
    """
    def __init__(self, src: str, title: str, artist: str, duration: int) -> None:
        self.src = src
        self.title = title
        self.artist = artist
        self.duration = duration

    def dictify(self) -> dict:
        """
        Returns a dictionary representation of the song.
        """
        return {
            "title": self.title,
            "artist": self.artist,
            "filename": self.src,
            "duration": self.duration
        }


default_song = _Song("default_music.mp3", "Kahoot / Harmony Hootenanny Lobby Music", "Add a song above to stop listening to this ", 64)



class SongScheduler:
    """
    Manages song scheduling and playback in a room.

    Attributes:
        room_id (int): The unique identifier for the room.
        socketio: The Socket.IO instance for real-time communication.
        check_interval (int): The interval (in seconds) at which the thread checks for updates.
        queue (list[_Song]): A list of queued songs.
        playing (bool): Indicates whether playback is currently active.
        scheduler_thread (Thread): The background thread for updating song playback.
        current_song (_Song): The currently playing song.
        timeout (int): Accumulated time when playback is paused.
        endtime (int): The timestamp when the current song playback should end.

    Methods:
        start_thread():
            Starts the scheduler thread.
        _updater_thread():
            The main thread function that manages song playback and updates.
        skip():
            Skips to the next song in the queue.
        pause():
            Pauses song playback.
        play() -> int:
            Resumes song playback and returns remaining playback time.
        add_to_queue(song_id: int):
            Adds a song to the queue based on its ID.
        get_queue() -> List[dict]:
            Returns a list of dictionaries representing songs in the queue.
        get_current_song() -> dict:
            Returns a dictionary with information about the currently playing song.
    """
    def __init__(self, room_id: int, socketio) -> None:
        example_queue = [
            _Song("Hypnotized.mp3", "Hypnotized", "Someone1", 195),
            _Song("Men At Work - Down Under (Official HD Video).mp3", "Down Under", "Men At Work", 220),
            _Song("Bob Marley - One Love.mp3","One Love", "Bob MArley", 164)
            ]
        self.room_id = room_id
        self.socketio = socketio
        self.check_interval = 1
        self.queue: list[_Song] = example_queue
        self.playing = True
        self.scheduler_thread = threading.Thread(target=self._updater_thread)
        self.current_song: _Song = default_song
        self.timeout = 0
        self.endtime = int(time.time()) + self.current_song.duration
    
    def start_thread(self) -> None:
        """Starts the scheduler thread."""
        self.scheduler_thread.start()

    def _updater_thread(self) -> None:
        """Main thread function for managing song playback and updates."""
        while True:
            if not self.playing:
                self.timeout += self.check_interval
            elif self.endtime + self.timeout <= int(time.time()):
                if len(self.queue) == 0:
                    self.current_song: _Song = default_song
                    self.timeout = 0
                    self.endtime = int(time.time()) + self.current_song.duration
                    self.socketio.emit("currently_playing", self.get_current_song(), room=self.room_id)
                else:
                    self.skip()
            time.sleep(self.check_interval)
                
    def skip(self) -> None:
        """Skips to the next song in the queue."""
        try:
            next_song: _Song = self.queue.pop(0)
        except Exception as e:
            next_song: _Song = default_song
        self.timeout = 0
        self.playing = True
        self.current_song = next_song
        self.endtime = (time.time()) + next_song.duration
        self.socketio.emit("currently_playing", self.get_current_song(), room=self.room_id)
        self.socketio.emit("song_queue", {"queue": self.get_queue()}, room=self.room_id)
      
    def pause(self) -> None:
        """Pauses song playback."""
        self.playing = False

    def play(self) -> int:
        """
        Resumes song playback and returns remaining playback time.

        Returns:
            int: Remaining playback time in seconds.
        """
        self.playing = True
        return self.current_song.duration - (self.endtime - time.time()) - self.timeout

    def add_to_queue(self, song_id: int) -> None:
        """Adds a song to the queue based on its ID."""
        song_props = get_song_by_id(song_id)
        #     def __init__(self, src: str, title: str, artist: str, duration: int) -> None:
        new_song = _Song(song_props["src"], song_props["title"], song_props["artist"],  song_props["duration"])
        self.queue.append(new_song)
        self.socketio.emit("song_queue", {"queue": self.get_queue()}, room=self.room_id)
    
    def get_queue(self) -> list[dict]:
        """Returns a list of dictionaries representing songs in the queue."""
        return [song.dictify() for song in self.queue]
        
    def get_current_song(self) -> dict[str, str | int]:
        """
        Returns a dictionary with information about the currently playing song.

        Returns:
            dict: Dictionary with keys:
                - "title": The song title.
                - "artist": The artist's name.
                - "filename": The source (file path or URL).
                - "progress": Remaining playback time in seconds.
        """
        return {
            "title": self.current_song.title,
            "artist": self.current_song.artist,
            "filename": self.current_song.src,
            "progress": self.current_song.duration - (self.endtime - time.time()) - self.timeout,
        }
