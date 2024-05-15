import time
import threading
from flask_socketio import emit
from database import get_next_song

class SongScheduler:
    def __init__(self, room_id, socketio):
        self.room_id = room_id
        self.socketio = socketio
        self.check_interval = 1  # Check every second
        self.current_song_end_time = None
        self.scheduler_thread = threading.Thread(target=self._check_song_completion, daemon=True)
        self.song_info = {}

    def add_song(self, song_start_time, duration):
        self.current_song_end_time = song_start_time + duration
        self.song_info[self.room_id] = (song_start_time, duration)

    def start_scheduler(self):
        print("Scheduler thread started for room:", self.room_id)
        self.scheduler_thread.start()

    def _check_song_completion(self):
        while True:
            current_time = time.time()
            if self.current_song_end_time and current_time >= self.current_song_end_time:
                self._next_song()
            time.sleep(self.check_interval)

    def _next_song(self):
        next_song = get_next_song(self.room_id)
        if next_song and 'duration' in next_song:
            start_time = time.time()
            duration = next_song['duration']
            self.add_song(start_time, duration)
            self.socketio.emit("currently_playing", {"track": next_song['filename'], "progress": 0}, room=self.room_id)
        else:
            self.current_song_end_time = None
            self.socketio.emit("currently_playing", {"track": None, "progress": 0}, room=self.room_id)
