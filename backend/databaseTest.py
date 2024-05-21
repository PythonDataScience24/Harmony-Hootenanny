import sqlite3
import logging

def get_stat(cursor, query, room_id):
    try:
        cursor.execute(query, (room_id,))
        result = cursor.fetchone()
        if result is None:
            logging.warning(f"Kein Ergebnis für Abfrage {query} mit room_id {room_id}")
            return None
        return result[0]
    except Exception as e:
        logging.error(f"Fehler beim Ausführen der Abfrage {query} mit room_id {room_id}: {e}")
        return None

try:
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    room_data = {}
    for room_id in [1, 2, 3]:
        room_data[f'room{room_id}'] = {
            'number_of_listeners': get_stat(cursor, "Select number_of_listeners FROM rooms WHERE room_id=?", room_id),
            'total_play_time': get_stat(cursor, "SELECT SUM(duration) FROM songs JOIN queues on songs.song_id = queues.song_id WHERE queues.room_id=?", room_id),
            'most_played_song': get_stat(cursor, """
                           SELECT title, COUNT(*) as count
                            FROM songs JOIN queues on songs.song_id = queues.song_id
                            WHERE queues.room_id=?
                            GROUP BY songs.song_id
                            ORDER BY count DESC
                            LIMIT 1
                            """, room_id),
            'top_artist': get_stat(cursor, """
                           SELECT artist, COUNT(*) as count
                            FROM songs JOIN queues on songs.song_id = queues.song_id
                            WHERE queues.room_id=?
                            GROUP BY artist
                            ORDER BY count DESC
                            LIMIT 1
                            """, room_id)
        }

    print(room_data)
    
except Exception as e:
    print(f"Fehler: {str(e)}")
finally:
    db.close()