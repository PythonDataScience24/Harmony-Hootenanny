CREATE TABLE IF NOT EXISTS rooms (
  room_id INTEGER PRIMARY KEY AUTOINCREMENT,
  number_of_listeners INTEGER,
  session_start_time DATETIME,
  session_end_time DATETIME,
  session_duration INTEGER
);
CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username Text,
  password_hash Text
);