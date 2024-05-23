from matplotlib import pyplot as plt

from database import get_db_connection
def get_stats(cursor, query, room_id):
    cursor.execute(query, (room_id,))
    rows = cursor.fetchall()
    return [{description[0]: value for description, value in zip(cursor.description, row)} for row in rows]
def get_stats2(cursor, query):
    cursor.execute(query,)
    rows = cursor.fetchall()
    return [{description[0]: value for description, value in zip(cursor.description, row)} for row in rows]


with get_db_connection() as db:
    cursor = db.cursor()
    room_id = 1
    data = {
                    'room_id': room_id,
                    'number_of_listeners': get_stats(cursor, "Select number_of_listeners FROM rooms WHERE room_id=?", room_id),
                    'total_play_time': get_stats(cursor, "SELECT SUM(duration) FROM songs JOIN queues on songs.song_id = queues.song_id WHERE queues.room_id=?", room_id),
                    'most_played_song': get_stats(cursor, """
                               SELECT title, COUNT(*) as count
                                FROM songs JOIN queues on songs.song_id = queues.song_id
                                WHERE queues.room_id=?
                                GROUP BY songs.song_id
                                ORDER BY count DESC
                                Limit 3
                                """, room_id),
                    'top_artist': get_stats(cursor, """
                               SELECT artist, COUNT(*) as count
                                FROM songs JOIN queues on songs.song_id = queues.song_id
                                WHERE queues.room_id=?
                                GROUP BY artist
                                ORDER BY count DESC
                                Limit 3
                                """, room_id),
                     'most_popular_actions': get_stats(cursor, """
                                SELECT action_type, COUNT(*) as count
                                FROM user_actions
                                WHERE room_id=?
                                GROUP BY action_type
                                ORDER BY count DESC
                                """, room_id),
                    'top_skipper': get_stats2(cursor, """
                               SELECT user_id, username, COUNT(*) as count
                                FROM user_actions  LEFT JOIN users USING(user_id)
                                WHERE action_type='skip_song'
                                GROUP BY user_id
                                ORDER BY count DESC
                                LIMIT 5
                                """),
                    'top_enqueuer': get_stats2(cursor, """
                               SELECT user_id, username, COUNT(*) as count
                                FROM user_actions  LEFT JOIN users USING(user_id)
                                WHERE action_type='enqueue_song'
                                GROUP BY user_id
                                ORDER BY count DESC
                                LIMIT 5
                                """)
                }
    
    # TOP ENQUEUERS
    x_data = [value["count"] for value in data["top_enqueuer"]]
    x_labels = [value["username"] for value in data["top_enqueuer"]]
    print(x_data, x_labels)
    plt.bar(x_labels, x_data, color ='maroon', 
        width = 0.4)
    plt.yticks([15,16,17,18,19,20,21])
    plt.ylim(15)
    plt.savefig("../frontend/public/topQueuers.png") 

    plt.clf()


    x_data = [value["count"] for value in data["top_skipper"]]
    x_labels = [value["username"] for value in data["top_skipper"]]
    print(x_data, x_labels)
    plt.bar(x_labels, x_data, color ='red', 
        width = 0.4)
    plt.yticks([15,16,17,18,19,20,21, 22])
    plt.ylim(15)
    plt.savefig("../frontend/public/topSkippers.png") 