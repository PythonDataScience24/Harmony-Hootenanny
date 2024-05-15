import time
import threading

class SongScheduler:
    def __init__(self, start_time, duration):
        self.check_interval = 1  # Check every second
        self.endtime = start_time + duration
        self.scheduler_thread = threading.Thread(target=self._check_song_completion, daemon=True)


    def add_song(self, room_id, song_start_time, duration):
        self.song_info[room_id] = (song_start_time, duration)

    def start_scheduler(self):
        self.scheduler_thread.start()

    def _check_song_completion(self):
        while True:
            current_time = int(time.time())
            if self.endtime <= current_time:
                    self.skip(room_id)
            time.sleep(self.check_interval)

    def skip(self, room_id):
        pass