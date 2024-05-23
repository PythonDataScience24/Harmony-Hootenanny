from matplotlib import pyplot as plt

from database import get_db_connection

"""
DO NOT JUDGE THIS FILE, IT HAS BEEN MADE IN 15 MINUTES, I KNOW THERE'S A LOT WRONG
"""

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
                    'number_of_listeners1': get_stats(cursor, "Select number_of_listeners FROM rooms WHERE room_id=?", 1),
                    'number_of_listeners2': get_stats(cursor, "Select number_of_listeners FROM rooms WHERE room_id=?", 2),
                    'number_of_listeners3': get_stats(cursor, "Select number_of_listeners FROM rooms WHERE room_id=?", 3),
                    'total_play_time1': get_stats(cursor, "SELECT SUM(duration) FROM songs JOIN queues on songs.song_id = queues.song_id WHERE queues.room_id=?", 1),
                    'total_play_time2': get_stats(cursor, "SELECT SUM(duration) FROM songs JOIN queues on songs.song_id = queues.song_id WHERE queues.room_id=?", 2),
                    'total_play_time3': get_stats(cursor, "SELECT SUM(duration) FROM songs JOIN queues on songs.song_id = queues.song_id WHERE queues.room_id=?", 3),
                    'most_played_song1': get_stats(cursor, """
                               SELECT title, COUNT(*) as count
                                FROM songs JOIN queues on songs.song_id = queues.song_id
                                WHERE queues.room_id=?
                                GROUP BY songs.song_id
                                ORDER BY count DESC
                                Limit 7
                                """, 1),
                    'most_played_song2': get_stats(cursor, """
                               SELECT title, COUNT(*) as count
                                FROM songs JOIN queues on songs.song_id = queues.song_id
                                WHERE queues.room_id=?
                                GROUP BY songs.song_id
                                ORDER BY count DESC
                                Limit 7
                                """, 2),
                    'most_played_song3': get_stats(cursor, """
                               SELECT title, COUNT(*) as count
                                FROM songs JOIN queues on songs.song_id = queues.song_id
                                WHERE queues.room_id=?
                                GROUP BY songs.song_id
                                ORDER BY count DESC
                                Limit 7
                                """, 3),                        
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
    plt.bar(x_labels, x_data, color ='maroon', 
        width = 0.4)
    plt.yticks([15,16,17,18,19,20,21])
    plt.ylim(15)
    plt.xlabel("username")
    plt.ylabel("number of songs added to queue")
    plt.savefig("../frontend/public/topQueuers.png") 

    plt.clf()
    x_data = [value["count"] for value in data["top_skipper"]]
    x_labels = [value["username"] for value in data["top_skipper"]]
    plt.bar(x_labels, x_data, color ='red', 
        width = 0.4)
    plt.yticks([15,16,17,18,19,20,21, 22])
    plt.ylim(15)
    plt.xlabel("username")
    plt.ylabel("number of songs skipped")
    plt.savefig("../frontend/public/topSkippers.png") 

    plt.clf()
    y_data = [value["count"] for value in data["most_played_song1"]]
    y_label = [value["title"] for value in data["most_played_song1"]]
    plt.pie(y_data, labels = y_label)
    plt.savefig("../frontend/public/topSongs1.png") 

    plt.clf()
    y_data = [value["count"] for value in data["most_played_song2"]]
    y_label = [value["title"] for value in data["most_played_song2"]]
    plt.pie(y_data, labels = y_label)
    plt.savefig("../frontend/public/topSongs2.png") 

    plt.clf()
    y_data = [value["count"] for value in data["most_played_song3"]]
    y_label = [value["title"] for value in data["most_played_song3"]]
    plt.pie(y_data, labels = y_label)

    plt.savefig("../frontend/public/topSongs3.png") 
    plt.clf()
    x_data = [[data["number_of_listeners1"]][0][0]["number_of_listeners"],[data["number_of_listeners2"]][0][0]["number_of_listeners"],[data["number_of_listeners3"]][0][0]["number_of_listeners"]]
    x_labels = ["Room 1", "Room 2", "Room 3"]
    plt.ylabel("number of people tuning in")
    plt.bar(x_labels, x_data, width = 0.4)
    plt.savefig("../frontend/public/numberOfListeners.png") 

    plt.clf()
    x_data = [data["total_play_time1"][0]['SUM(duration)'],data["total_play_time2"][0]['SUM(duration)'],data["total_play_time3"][0]['SUM(duration)']]
    x_labels = ["Room 1", "Room 2", "Room 3"]
    plt.ylabel("total minutes played")
    plt.bar(x_labels, x_data, width = 0.4)
    plt.savefig("../frontend/public/playtime.png") 
    

