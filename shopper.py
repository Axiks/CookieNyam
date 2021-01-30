import sqlite3

class Shopper:
  def __init__(self, user_id, name=None):
    self.__user_id = user_id
    self.__name = name

# ID
  def getId(self):
    return self.__user_id

# Iм`я
  def getName(self):
    if self.__name == None:
        conn = sqlite3.connect('cookie.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT user_name FROM Cookie WHERE user_id=" + str(self.__user_id) + " ORDER BY get_data DESC LIMIT 1")
        user = cursor.fetchone()
        self.__name = user[0]
        conn.close()
    return self.__name

# Усього печеньок
  def cookieCountAll(self):
    conn = sqlite3.connect('cookie.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Cookie WHERE user_id=" + str(self.__user_id))
    count_cookie = cursor.fetchone()[0]
    conn.close()
    return count_cookie