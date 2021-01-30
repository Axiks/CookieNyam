import sqlite3

class Statistic:
    def __init__(self, chat_id=None):
        self.__chat_id = chat_id

    def all_cookies_distributed():
        conn = sqlite3.connect('cookie.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Cookie")
        count_cookie = cursor.fetchone()[0]
        conn.close()
        return count_cookie

    def all_users_uses():
        conn = sqlite3.connect('cookie.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM Cookie")
        count_cookie = cursor.fetchone()[0]
        conn.close()
        return count_cookie

    def all_chat_uses():
        conn = sqlite3.connect('cookie.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT chat_id) FROM Cookie")
        count_cookie = cursor.fetchone()[0]
        conn.close()
        return count_cookie