from database import get_db_connection

def get_user_id(username):
    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result[0] if result else None
