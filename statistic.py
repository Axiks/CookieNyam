import sqlite3
from config.config import DATABASE_PATH

class Statistic:
    def all_cookies_distributed():
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Cookie")
        count_cookie = cursor.fetchone()[0]
        conn.close()
        return count_cookie

    def all_users_uses():
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM Cookie")
        count_cookie = cursor.fetchone()[0]
        conn.close()
        return count_cookie

    def all_chat_uses():
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT chat_id) FROM Cookie")
        count_cookie = cursor.fetchone()[0]
        conn.close()
        return count_cookie