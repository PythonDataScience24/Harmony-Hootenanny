CREATE TABLE IF NOT EXISTS rooms (
  room_id INTEGER PRIMARY KEY,
  number_of_listeners INTEGER,
  session_start_time DATETIME,
  session_end_time DATETIME,
  session_duration INTEGER,
  song_start_time DATETIME,
  queue_index INTEGER REFERENCES queues (queue_index)
);
CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username Text,
  password_hash Text
);
CREATE TABLE IF NOT EXISTS songs (
  song_id INTEGER PRIMARY KEY AUTOINCREMENT,
  src Text,
  title Text,
  artist Text,
  duration INTEGER
);
CREATE TABLE IF NOT EXISTS queues (
  queue_index INTEGER PRIMARY KEY AUTOINCREMENT,
  song_id INTEGER REFERENCES songs (song_id),
  room_id INTEGER REFERENCES rooms (room_id),
  user_id INTEGER REFERENCES users (user_id)
);