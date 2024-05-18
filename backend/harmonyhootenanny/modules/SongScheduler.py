

import threading
import time
from ..extensions import socketio
from flask_socketio import emit
from database import get_queue, get_song

class _Song:
    def __init__(self, src: str, title: str, artist: str, duration: int) -> None:
        self.src: str = src
        self.title: str = title
        self.artist: str = artist
        self.duration:int  = duration

    def dictify(self):
        return {
            "title": self.title, 
            "artist":self.artist, 
            "filename":self.src, 
            "duration": self.duration
        }


default_song = _Song("test.mp3", "No Songs added yet", "Me, Myself & I", 5)



class SongScheduler:
    def __init__(self, room_id: int, socketio) -> None:
        example_queue = [
    _Song("Hypnotized.mp3", "Hypnotized", "Someone1", 195),
    _Song("Men At Work - Down Under (Official HD Video).mp3", "Down Under", "Men At Work", 220),
    _Song("Bob Marley - One Love.mp3","One Love", "Bob MArley", 164)
]
        self.room_id = room_id
        self.socketio = socketio
        self.check_interval = 1 # amount of seconds before thread checks for updates
        self.queue: list[_Song] = example_queue
        self.playing = True
        self.scheduler_thread = threading.Thread(target=self._updater_thread)
        self.current_song: _Song = default_song
        self.timeout = 0
        self.endtime = int(time.time()) + self.current_song.duration
    
    def start_thread(self):
        self.scheduler_thread.start()

    def _updater_thread(self):
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
                
    def skip(self):
        next_song: _Song = self.queue.pop(0)
        self.timeout = 0
        self.playing = True
        self.current_song = next_song
        self.endtime = (time.time()) + next_song.duration
        self.socketio.emit("currently_playing", self.get_current_song(), room=self.room_id)
        self.socketio.emit("song_queue", {"queue": self.get_queue()}, room=self.room_id)
      
    def pause(self):
        self.playing = False

    def play(self):
        self.playing = True
        return self.current_song.duration - (self.endtime - time.time()) - self.timeout

    def add_to_queue(self, song_id: int):
        song_props = get_song(song_id)
        new_song = _Song(song_props[0], song_props[1], song_props[2], song_props[3])
        self.queue.append(new_song)
    
    def get_queue(self):
        return [song.dictify() for song in self.queue]
        
    def get_current_song(self):         
        return {
            "title": self.current_song.title, 
            "artist":self.current_song.artist, 
            "filename":self.current_song.src, 
            "progress": self.current_song.duration - (self.endtime - time.time()) - self.timeout,
        }



