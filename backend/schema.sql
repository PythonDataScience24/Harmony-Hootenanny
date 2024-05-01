CREATE TABLE IF NOT EXISTS rooms (
  room_id INTEGER PRIMARY KEY AUTOINCREMENT,
  number_of_listeners INTEGER,
  session_start_time DATETIME,
  session_end_time DATETIME,
  session_duration INTEGER
);