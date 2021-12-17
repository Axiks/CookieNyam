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

from config.config import TOKEN, COOKIE_COOKING_TIME, DATABASE_PATH, VERSION
from shopper import Shopper
from baker import Baker
from statistic import Statistic

# sqlite
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# program
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# keyboard
inline_btn_get_cookie = InlineKeyboardButton(emoji.emojize(":cookie:") + ' Взяти', callback_data='get_btn')
inline_btn_cooking_time = InlineKeyboardButton(emoji.emojize(":woman_cook:") + ' Розклад випічки', callback_data='timetable_btn')

inline_kb_get_cookie = InlineKeyboardMarkup(row_width=2)
inline_kb_get_cookie.insert(inline_btn_get_cookie)
inline_kb_get_cookie.insert(inline_btn_cooking_time)

#Command cmd
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    img = open('src/new_chat_members.png', 'rb')
    await bot.send_photo(message.chat.id, img)
    await bot.send_message(message.chat.id, "Привіт :3\nЯ неко-тян. Люблю пекти смачні 2D печеньки.\nВласне хочу з вами ними поділитись!\nПечу їх " + str(len(COOKIE_COOKING_TIME)) + " раз на день.\nЩоб дізнатись більше про мене напишіть команду /help")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    help_msg = "Я неко пекар яка любить випікати смачне печиво, а ще більше ділитись ним з оточуючими)\nДостатньо запросити мене у чат\nЩоб дізнатись мої команди напиши /commands \n\nМене створив @Qweeik\n2021 {0}\nCode source: https://github.com/Axiks/CookieNyam\nУсього спечено печення: *".format(VERSION) + str(Statistic.all_cookies_distributed()) + "*\nУсього користувачів що взяли печення: *" + str(Statistic.all_users_uses()) + "*\nВипікаю печення для: *" + str(Statistic.all_chat_uses()) + "* чатів"
    await bot.send_message(message.chat.id, help_msg, parse_mode= 'Markdown')

@dp.message_handler(commands=['nya'])
async def process_nya_command(message: types.Message):
    await bot.send_message(message.chat.id, "Nya nya :3")

@dp.message_handler(commands=['commands'])
async def process_nya_command(message: types.Message):
    commands_msg ="""
    /start - запускає мене\n
    /teleport - переміщую тебе ближче до смаколиків\n
    /help - нюю.. Розказую хто я і хто мій засновни. А ще можеш побачити мене без печенюшок на GitHub ~
    """;
    await bot.send_message(message.chat.id, commands_msg)

# @dp.message_handler(commands=['transfer'])
# async def process_nya_command(message: types.Message):
#     amount = 2
#     nekoA = Shopper(message.from_user.id)
#     nekoB = Shopper(472737067)
#     status = await transfer_cookie(nekoA.getId(), nekoB.getId(), amount, message.chat.id)
#     print("Transfer status: " + str(status))
#     await bot.send_message(message.chat.id, nekoA.getName() + " дав " + nekoB.getName() + " " + str(amount) + " печив.")
#     await bot.send_message(message.chat.id, nekoA.getName() + " має " + str(nekoA.cookieCountAll()) + " печива.\n" + nekoB.getName() + " тепер має " + str(nekoB.cookieCountAll()) + " печива.\n")


@dp.message_handler(commands=['teleport'])
async def process_teleport_command(message: types.Message):
    nekoBaker = Baker(message.chat.id, COOKIE_COOKING_TIME)
    message_id = nekoBaker.last_baking_message_id
    if message_id is not None:
        if message.chat.username is not None:
            # keyboard
            inline_kb_tl = InlineKeyboardMarkup(row_width=1)
            inline_btn_teleport = InlineKeyboardButton('Телепортуватись!', url= await url_go_message(message.chat.username , message_id))
            inline_kb_tl.insert(inline_btn_teleport)
            await bot.send_message(message.chat.id, "Ти викликав О великий І могутній телепорт", reply_markup=inline_kb_tl)
        else:
            await bot.send_message(message.chat.id, "^ Телепорт до печива ^", reply_to_message_id = message_id)

@dp.message_handler(content_types=["new_chat_members"])
async def new_chat(message: types.Message):
    for user in message.new_chat_members:
        if user.id == bot.id:
            img = open('src/new_chat_members.png', 'rb')
            await bot.send_photo(message.chat.id, img)
            await bot.send_message(message.chat.id, "Привіт :3\nЯ неко-тян. Люблю пекти смачні 2D печеньки.\nВласне хочу з вами ними поділитись!\nПечу їх " + str(len(COOKIE_COOKING_TIME)) + " раз на день.")
            new_chat_add(message.chat.id)
            print("Added to group")
            await cooking_post(message.chat.id)
            return

#Inline (Кнопки)
@dp.callback_query_handler(lambda c: c.data == 'timetable_btn')
async def process_start_command(callback_query: types.CallbackQuery):
    timetable = "Неко тян готує їх " + str(len(COOKIE_COOKING_TIME)) + " раз на день.\n\nРозклад\n"
    for cookie_time in COOKIE_COOKING_TIME:
        timetable = timetable + " - " + str(cookie_time) + "\n"
    await bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=True, text=timetable)

@dp.callback_query_handler(lambda callback_query: True)
async def callback_inline(callback_query):
    # Если сообщение из чата с ботом
    if callback_query.message:
        if callback_query.data == "get_btn":
            if callback_query.message.chat.id == callback_query.from_user.id:
                print("Get cookie from chat BOT")
                await bot.send_message(callback_query.message.chat.id, "Привіт)\nЯ не роздаю печиво тут!\nШукай мене там де багато людей :3\nАбо запроси мене у свій любимий чатик)")
                await bot.answer_callback_query(callback_query_id=callback_query.id)
            else:
                nekoBaker = Baker(callback_query.message.chat.id, COOKIE_COOKING_TIME)
                status = nekoBaker.get_cookie(callback_query.from_user.id, callback_query.from_user.full_name)
                if status:
                    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=renderGetCookieUsers(callback_query.message.chat.id), parse_mode= 'Markdown', reply_markup=inline_kb_get_cookie)
                    await bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False, text="Печенька взята!")
                else:
                    await bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=True, text="Ти брав печеньку!\nНе рухай.")
    # Если сообщение из инлайн-режима
    elif callback_query.inline_message_id:
        if callback_query.data == "get_btn":
            await bot.edit_message_text(inline_message_id=callback_query.inline_message_id, text="Inline Бдыщь")

#Code
def new_chat_add(chat_id):
    cursor.execute("SELECT COUNT(*) FROM Chat WHERE chat_id=" + str(chat_id))
    count_chat = cursor.fetchone()[0]
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if count_chat <= 0:
        cursor.execute("insert into Chat values (" + str(chat_id) + ", 'TRUE', '3','" + dt_string + "', '" + str(0) + "') ")
        conn.commit()
        return True
    return False

#Helpers
async def url_go_message(chat_id, message_id):
    url = "https://t.me/" + str(chat_id) + "/" + str(message_id)
    return url

#Money
# async def transfer_cookie(from_neko_id, in_neko_id, amount, chat_id):
#     nekoA = Shopper(from_neko_id)
#     if(nekoA.cookieCountAll() >= amount):
#         #Delete cookie Neko A
#         now = datetime.now()
#         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#         cursor.execute("insert into Cookie values (" + str(nekoA.getId()) + ", '" + str(nekoA.getName()) + "', '-" + str(amount) + "', " + str(chat_id) + ', "'  + dt_string + '")')
#         conn.commit()
#         #Delete cookie Neko B
#         nekoB = Shopper(in_neko_id)
#         now = datetime.now()
#         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#         cursor.execute("insert into Cookie values (" + str(nekoB.getId()) + ", '" + str(nekoB.getName()) + "', '" + str(amount) + "', " + str(chat_id) + ', "'  + dt_string + '")')
#         conn.commit()
#         return True
#     else:
#         print("Не достатньо печеньок для відправки")
#         return False


#Render
def renderGetCookieUsers(chat_id):
    text = "Печеньки готові :3\n\nПеченьку взяв:\n"
    nekoBaker = Baker(chat_id, COOKIE_COOKING_TIME)
    date_last_baking_cookie = nekoBaker.last_baking().strftime("%d/%m/%Y %H:%M:%S")
    #When user get last cookie? + FIX
    cursor.execute("SELECT DISTINCT user_id FROM Cookie WHERE chat_id=" + str(chat_id) + ' AND get_data >= "' + str(date_last_baking_cookie) + '" ORDER BY get_data DESC')
    cookies = cursor.fetchall()
    for cookie in cookies:
        user_id = cookie[0]
        user = Shopper(user_id)
        text = text + "+1 *" + str(user.getName()) + "* має тепер " + str(user.cookieCountAll()) + " печеньок\n"
    return text

#Cooking Post
async def cooking_post(chat_id):
    img = open('src/cookie_cooking.gif', 'rb')
    try:
        await bot.send_animation(chat_id, img, 10)
        message_obj = await bot.send_message(chat_id, "Печеньки готові :3", reply_markup=inline_kb_get_cookie)
        message_id = message_obj.message_id
        print("Message ID: " + str(message_id))

        #UPDATE DB
        cursor.execute("UPDATE Chat SET cookies_have = 3, message_id = " + str(message_id) + " WHERE chat_id = " + str(chat_id))
        conn.commit()
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
    except:
        "Чото не працює..."
    print("Cookie cooking!")

#Auto time job
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