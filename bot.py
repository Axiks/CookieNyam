from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import asyncio
import aioschedule

import emoji

import sqlite3

from datetime import datetime, timedelta

from config import TOKEN, START_COOKIE_COUNT, COOKIE_COOKING_TIME

# sqlite
conn = sqlite3.connect('cookie.sqlite')
cursor = conn.cursor()

# keyboard
inline_kb = InlineKeyboardMarkup(row_width=2)
inline_btn_get_cookie = InlineKeyboardButton(emoji.emojize(":cookie:") + ' Взяти', callback_data='button1')
inline_btn_number_of_cookie = InlineKeyboardButton('Скільки печеньок маю?', callback_data='button2')
inline_btn_test = InlineKeyboardButton('Test', callback_data='test')
inline_kb.insert(inline_btn_get_cookie)
inline_kb.insert(inline_btn_number_of_cookie)
inline_kb.insert(inline_btn_test)


inline_kb_help = InlineKeyboardMarkup(row_width=1)
inline_btn_cooking_time = InlineKeyboardButton(emoji.emojize(":woman_cook:") + ' Розклад випічки', callback_data='button3')
inline_kb_help.insert(inline_btn_cooking_time)
inline_kb_help.insert(inline_btn_test)

inline_kb_get_cookie = InlineKeyboardMarkup(row_width=2)
inline_kb_get_cookie.insert(inline_btn_get_cookie)
inline_kb_get_cookie.insert(inline_btn_cooking_time)

# button_get_cookie = KeyboardButton('Хочу печеньку!')
# button_number_of_cookie = KeyboardButton('Кількість моїх печеньок')

# greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
# greet_kb.add(button_get_cookie)
# greet_kb.add(button_number_of_cookie)


# program
COOKIE_AVAILABLE = START_COOKIE_COUNT

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def get_cookie(chat_id, user_id, user_name):
    print("USer id: " + str(user_id))
    print("Chat id: " + str(chat_id))

    # user_id = "783550633"
    # chat_id = "-1001413747213"

    if chat_id == user_id:
        print("Get cookie from chat BOT")
        return False

    #When user get last cookie? + FIX
    cursor.execute("SELECT get_data FROM Cookie WHERE chat_id=" + str(chat_id) + ' AND user_id=' + str(user_id) + ' ORDER BY get_data DESC LIMIT 1')
    cookie = cursor.fetchone()
    cookie_cooking_time_user = "01/01/2000 00:00:00" #fix
    if cookie is None:
        print("New user in chat")
    else:
        cookie_cooking_time_user = cookie[0]
    user_last_get_cookies_time_obj = datetime.strptime(cookie_cooking_time_user, "%d/%m/%Y %H:%M:%S")

    #Get Cookie?
    date_last_baking_cookie = time_last_baking()
    print("Last baking data: " + date_last_baking_cookie.strftime("%d/%m/%Y %H:%M:%S"))
    print("Last USER get Cookie: " + user_last_get_cookies_time_obj.strftime("%d/%m/%Y %H:%M:%S"))
    if date_last_baking_cookie > user_last_get_cookies_time_obj:
        # add cookie db
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        cursor.execute("insert into Cookie values (" + str(user_id) + ", '" + str(user_name) + "', '1', " + str(chat_id) + ', "'  + dt_string + '")')
        conn.commit()
        print(str(user_id) + "взяв печеньку")
        return True
    print("Не можна брати печеньки")
    return False

async def url_go_message(chat_id, message_id):
    #https://t.me/AnimeOChat/116500
    url = "https://t.me/" + str(chat_id) + "/" + str(message_id)
    print(url)
    return url

def number_of_cookies_chat(chat_id):
    count_cookie = 0
    try:
        #Тут може виникати баги з розмовою з самим ботом
        cursor.execute("SELECT cookies_have FROM Chat WHERE chat_id=" + str(chat_id))
        count_cookie = cursor.fetchone()[0]
    except:
        print("Exept error number_of_cookies_chat")
    return count_cookie

def my_cookie_count(user_id):
    cursor.execute("SELECT COUNT(*) FROM Cookie WHERE user_id=" + str(user_id))
    count_cookie = cursor.fetchone()[0]
    return count_cookie

def new_chat_add(chat_id):
    cursor.execute("SELECT COUNT(*) FROM Chat WHERE chat_id=" + str(chat_id))
    count_chat = cursor.fetchone()[0]

    now = datetime.now()
    print("now =", now)
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)

    if count_chat <= 0:
        cursor.execute("insert into Chat values (" + str(chat_id) + ", 'TRUE', '" + str(START_COOKIE_COUNT) + "','" + dt_string + "', '" + str(0) + "') ")
        conn.commit()
        return True
    return False

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    #await message.reply("Привіт!\nНеко-тян приготує для тебе найсмачніші 2D печеньки!", reply_markup=inline_kb_get_cookie)
    img = open('new_chat_members.png', 'rb')
    await bot.send_photo(message.chat.id, img)
    await bot.send_message(message.chat.id, "Привіт :3\nЯ неко-тян. Люблю пекти смачні 2D печеньки.\nВласне хочу з вами ними поділитись!\n Печу їх " + str(len(COOKIE_COOKING_TIME)) + " раз на день.", reply_markup=inline_kb_get_cookie)

@dp.message_handler(commands=['nya'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Nya nya :3", reply_markup=inline_kb_get_cookie)


# @dp.message_handler(commands=['test'])
# async def process_start_command(message: types.Message):
#     print_str = ""
#     now = datetime.now()
#     dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
#     print_str = print_str + "\nServer data: " + dt_string
#     print(time_last_baking())
#     await message.reply("I work!" + print_str + "\nЧас останньої випічки: " + str(time_last_baking()), reply_markup=inline_kb)

# @dp.callback_query_handler(lambda c: c.data == 'button1')
# async def process_callback_button1(callback_query: types.CallbackQuery):
#     #await bot.answer_callback_query(callback_query.id)
#     # await bot.send_message(callback_query.message.chat.id, 'Натиснута кнопка для отримання печеньок!')
#     # await bot.send_message(callback_query.from_user.id, 'Натиснута кнопка для отримання печеньок!')
#     if get_cookie(callback_query.message.chat.id, callback_query.from_user.id, callback_query.from_user.full_name):
#         await bot.send_message(callback_query.message.chat.id, callback_query.from_user.full_name + " взяв печеньку!\n", reply_markup=inline_kb_get_cookie)
#         await bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False, text="Печенька взята!")
#     else:
#         #await bot.send_message(callback_query.message.chat.id, callback_query.from_user.full_name + " ти уже брав печеньку!\nНе рухай..", reply_markup=inline_kb_help)
#         await bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=True, text="А ну не трож печеньки!")

@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_start_command(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    await bot.send_message(callback_query.message.chat.id, callback_query.from_user.full_name + " має: " + str(my_cookie_count(user_id)) + " смачних печеньок")

@dp.callback_query_handler(lambda c: c.data == 'button3')
async def process_start_command(callback_query: types.CallbackQuery):
    timetable = "Неко тян готує їх " + str(len(COOKIE_COOKING_TIME)) + " раз на день.\n\nРозклад\n"
    for cookie_time in COOKIE_COOKING_TIME:
        timetable = timetable + " - " + str(cookie_time) + "\n"
    #await bot.send_message(callback_query.message.chat.id, callback_query.from_user.full_name + " ти можеш отримати печеньку згодом!\n" + timetable)
    #await bot.answer_callback_query(callback_query.id)
    await bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=True, text=timetable)
# @dp.message_handler(commands=['help'])
# async def process_help_command(message: types.Message):
#     await message.reply("Ти можеш отримати печеньку!\n Неко тян готує їх 2-чі на день по 3 штуки.\n\nРозклад\n10:00\n22:00")

# В большинстве случаев целесообразно разбить этот хэндлер на несколько маленьких

@dp.callback_query_handler(lambda callback_query: True)
async def callback_inline(callback_query):
    # Если сообщение из чата с ботом
    if callback_query.message:
        if callback_query.data == "button1":
            if get_cookie(callback_query.message.chat.id, callback_query.from_user.id, callback_query.from_user.full_name):
                #await bot.send_message(callback_query.message.chat.id, callback_query.from_user.full_name + " взяв печеньку!\n", reply_markup=inline_kb_get_cookie)
                await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=renderGetCookieUsers(callback_query.message.chat.id), parse_mode= 'Markdown', reply_markup=inline_kb_get_cookie)
                # # # await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
                # # # await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id - 1)
                # # # await cookking_update_post(callback_query.message.chat.id)
                await bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False, text="Печенька взята!")
            else:
                #await bot.send_message(callback_query.message.chat.id, callback_query.from_user.full_name + " ти уже брав печеньку!\nНе рухай..", reply_markup=inline_kb_help)
                await bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=True, text="Ти брав печеньку!\nНе рухай.")
    # Если сообщение из инлайн-режима
    elif callback_query.inline_message_id:
        if callback_query.data == "button1":
            await bot.edit_message_text(inline_message_id=callback_query.inline_message_id, text="Inline Бдыщь")

@dp.message_handler(commands=['neko'])
async def process_start_command(message: types.Message):
    await cooking_post(message.chat.id)

@dp.message_handler(commands=['teleport'])
async def process_start_command(message: types.Message):
    # await message.reply('Привет!\nИспользуй /help, '
    #                     'чтобы узнать список доступных команд!')
    cursor.execute("SELECT message_id FROM Chat WHERE chat_id=" + str(message.chat.id) + " ORDER BY message_id DESC LIMIT 1")
    chat = cursor.fetchone()
    message_id = chat[0]
    if message_id is not None:
        if message.chat.username is not None:
            # keyboard
            inline_kb_tl = InlineKeyboardMarkup(row_width=1)
            inline_btn_teleport = InlineKeyboardButton('Телепортуватись!', url= await url_go_message(message.chat.username , message_id))
            inline_kb_tl.insert(inline_btn_teleport)
            await bot.send_message(message.chat.id, "Ти викликав О великий І могучий телепорт", reply_markup=inline_kb_tl)
        else:
            await bot.send_message(message.chat.id, "^ Телепорт до печеньок ^", reply_to_message_id = message_id)

@dp.message_handler(content_types=["new_chat_members"])
async def new_chat(message: types.Message):
    """
    Handler for "new_chat_members" action when bot is added to chat.
    A special check is performed so that this handler will only be fired once per chat, when
    bot itself is added to group (bot's ID is the first part of token before ":" symbol)
    :param message: Telegram message with "new_chat_members" field not empty
    """
    for user in message.new_chat_members:
        if user.id == bot.id:
            img = open('new_chat_members.png', 'rb')
            await bot.send_photo(message.chat.id, img)
            await bot.send_message(message.chat.id, "Привіт :3\nЯ неко-тян. Люблю пекти смачні 2D печеньки.\nВласне хочу з вами ними поділитись!\nПечу їх " + str(len(COOKIE_COOKING_TIME)) + " раз на день.")
            new_chat_add(message.chat.id)
            print("Added to group")
            await cooking_post(message.chat.id)
            return

#Render
def renderGetCookieUsers(chat_id):
    text = "Печеньки готові :3\n\nПеченьку взяв:\n"
    date_last_baking_cookie = time_last_baking().strftime("%d/%m/%Y %H:%M:%S")
    #When user get last cookie? + FIX
    cursor.execute("SELECT user_id, user_name, get_data FROM Cookie WHERE chat_id=" + str(chat_id) + ' AND get_data >= "' + str(date_last_baking_cookie) + '" ORDER BY get_data DESC')
    cookies = cursor.fetchall()
    for cookie in cookies:
        user_id = cookie[0]
        user_name = cookie[1]
        # ChatMember = await bot.get_chat_member(chat_id= chat_id, user_id= user_id)
        # neme = ChatMember.user.full_name
        text = text + "+1 *" + str(user_name) + "* має тепер " + str(my_cookie_count(user_id)) + " печеньок\n"
    return text

#Kitchen
def time_last_baking():
    now_datime = datetime.now()

    #Generate baking date today
    now_date = now_datime.date()
    cookie_baking_date = []
    #   Add the last time last day
    last_baking_time = COOKIE_COOKING_TIME[len(COOKIE_COOKING_TIME)-1]
    last_baking_time_obj = datetime.strptime(last_baking_time, "%H:%M").time()
    probable_baking_date_yesterday = datetime.combine(now_date - timedelta(days=1), last_baking_time_obj)
    cookie_baking_date.append(probable_baking_date_yesterday)
    # Add today baking date
    for time in COOKIE_COOKING_TIME:
        baking_time_obj = datetime.strptime(time, "%H:%M").time()
        probable_baking_date = datetime.combine(now_date, baking_time_obj)
        cookie_baking_date.append(probable_baking_date)

    #Finding the date of the last bakin
    last_prop_date = cookie_baking_date[0]
    for prop_baking_date in cookie_baking_date:
        if prop_baking_date < now_datime:
            last_prop_date = prop_baking_date
        else:
            break
    return last_prop_date

# async def cookking_update_post(chat_id):
#     img = open('cookie_cooking.gif', 'rb')
#     try:
#         await bot.send_photo(chat_id, img)
#         message_obj = await bot.send_message(chat_id, text=renderGetCookieUsers(chat_id), reply_markup=inline_kb_get_cookie)
#         message_id = message_obj.message_id
#         #UPDATE DB
#         cursor.execute("UPDATE Chat SET message_id = " + str(message_id) + " WHERE chat_id = " + str(chat_id))
#         conn.commit()
#     except:
#         "Чото не працює..."

#Cooking Post

async def cooking_post(chat_id):
#Send Message
    img = open('cookie_cooking.gif', 'rb')
    try:
        #await bot.send_photo(chat_id, img)
        await bot.send_animation(chat_id, img, 10)
        message_obj = await bot.send_message(chat_id, "Печеньки готові :3", reply_markup=inline_kb_get_cookie)
        message_id = message_obj.message_id
        print("Message ID: " + str(message_id))

        #UPDATE DB
        #cookie_count_add = cookies_have + COOKIE_AVAILABLE
        cookie_count_add = COOKIE_AVAILABLE
        cursor.execute("UPDATE Chat SET cookies_have = " + str(cookie_count_add) + ", message_id = " + str(message_id) + " WHERE chat_id = " + str(chat_id))
        conn.commit()
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
    except:
        "Чото не працює..."
    print("Cookie cooking!")

#auto time job
async def cookie_cooking():
    cursor.execute("SELECT chat_id FROM Chat")
    chats = cursor.fetchall()
    for chat in chats:
        chat_id = chat[0]
        #Send Message
        await cooking_post(chat_id)


async def scheduler():
    for cook_time in COOKIE_COOKING_TIME:
        aioschedule.every().day.at(cook_time).do(cookie_cooking)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(x):
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)