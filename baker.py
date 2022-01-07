import sqlite3
from datetime import datetime, timedelta
from shopper import Shopper
from config.config import DATABASE_PATH

class Baker:
    def __init__(self, chat_id, cooking_time):
        self._chat_id = chat_id
        self._cooking_time = cooking_time

    # Просити печеньки
    def get_cookie(self, user_id, user_name):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        #When user get last cookie? + FIX
        query = "SELECT get_data FROM Cookie WHERE chat_id=" + str(self._chat_id) + ' AND user_id=' + str(user_id) + " ORDER BY rowid  DESC LIMIT 1";
        # print(query)
        cursor.execute(query)
        cookie = cursor.fetchone()
        cookie_cooking_time_user = "01/01/2000 00:00:00" #fix
        if cookie is None:
            print("New user get cookie in chat")
        else:
            cookie_cooking_time_user = cookie[0]

        print("cookie_cooking_time_user")
        print(cookie_cooking_time_user)


        user_last_get_cookies_time_obj = datetime.strptime(cookie_cooking_time_user, "%d/%m/%Y %H:%M:%S")

        #Get Cookie?
        date_last_baking_cookie = self.last_baking()
        print("Last baking data: " + date_last_baking_cookie.strftime("%d/%m/%Y %H:%M:%S"))
        print("Last USER get Cookie: " + user_last_get_cookies_time_obj.strftime("%d/%m/%Y %H:%M:%S"))

        # сравнить 
        if date_last_baking_cookie > user_last_get_cookies_time_obj:
            # add cookie db
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            cursor.execute("insert into Cookie values (" + str(user_id) + ", '" + str(user_name) + "', '1', " + str(self._chat_id) + ', "'  + dt_string + '")')
            conn.commit()
            print(str(user_id) + "взяв печеньку")
            return True
        print("Не можна брати печеньки")
        return False

    # Час останнього випікання
    def last_baking(self):
        now_datime = datetime.now() #Сьогоднішня дата

        #Generate baking date today
        now_date = now_datime.date() #Сьогоднішня дата?
        cookie_baking_date = []

        #   Add the last time last day
        last_baking_time = self._cooking_time[len(self._cooking_time)-1] # Останній час випікання
        last_baking_time_obj = datetime.strptime(last_baking_time, "%H:%M").time() ##Останній час в дата об'єкті

        probable_baking_date_yesterday = datetime.combine(now_date - timedelta(days=1), last_baking_time_obj) # ймовірна_дата_випічки_вчора
        cookie_baking_date.append(probable_baking_date_yesterday)

        # print("probable_baking_date_yesterday");
        # print(probable_baking_date_yesterday);

        # Add today baking date
        for time in self._cooking_time:
            baking_time_obj = datetime.strptime(time, "%H:%M").time() ##T
            probable_baking_date = datetime.combine(now_date, baking_time_obj)
            cookie_baking_date.append(probable_baking_date)
            # print("probable_baking_date");
            # print(probable_baking_date);


        #Finding the date of the last bakin
        last_prop_date = cookie_baking_date[0]
        for prop_baking_date in cookie_baking_date:
            if prop_baking_date < now_datime:
                last_prop_date = prop_baking_date
            else:
                break
        # print("last_prop_date");
        # print(last_prop_date);
        return last_prop_date

        # Id повідомлення про останнє випікання
    def last_baking_message_id(self):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT message_id FROM Chat WHERE chat_id=" + str(self._chat_id) + " ORDER BY message_id DESC LIMIT 1")
        chat = cursor.fetchone()
        message_id = chat[0]
        conn.close()
        return message_id