import sqlite3
from config.config import DATABASE_PATH

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
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT user_name FROM Cookie WHERE user_id=" + str(self.__user_id) + " ORDER BY get_data DESC LIMIT 1")
        user = cursor.fetchone()
        self.__name = user[0]
        conn.close()
    return self.__name

# Усього печеньок
  def cookieCountAll(self):
    balance = 0
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM Cookie WHERE user_id=" + str(self.__user_id))
    cookies = cursor.fetchall()
    for cookie in cookies:
        transaction = int(cookie[0])
        balance += transaction
    conn.close()
    return balance