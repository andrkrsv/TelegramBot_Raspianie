from random import random, randint
import telebot
from telebot import types
import sqlite3
bot = telebot.TeleBot('PLACE YOUR TOKEN')

markup2 = types.ReplyKeyboardMarkup()
btn3 = types.KeyboardButton('Login')
markup2.row(btn3)

markup4 = types.ReplyKeyboardMarkup()
btn1 = types.KeyboardButton('Функции')
btn2 = types.KeyboardButton('Report a bug')
markup4.row(btn1,btn2)

markup = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Удалить', callback_data = 'delete')
markup.row(btn1)

markup5 = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Сменить способ авторизации', callback_data = 'another_auth_method')
markup5.row(btn1)

markup3 = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Github', callback_data = 'github_auth')
btn2 = types.InlineKeyboardButton('Telegram', callback_data = 'telelogin')
btn3 = types.InlineKeyboardButton('Без авторизации', callback_data = 'no_auth')
btn4 = types.InlineKeyboardButton('Вроде красива', сallback_data = 'khui')
markup3.row(btn1,btn2)
markup3.row(btn3,btn4)

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('user-end.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f"hello! {message.from_user.first_name}", reply_markup=markup2)
    bot.send_message(message.chat.id, '<b>Выберите способ авторизации:</b>', parse_mode='html', reply_markup=markup3)

@bot.message_handler(func=lambda message: message.text == 'Функции')
def fuck(message):
    bot.send_message(message.chat.id,"собственно моя часть готова и что дальше делать я хз честн")
    bot.send_message(message.chat.id, "на кубик")
    pidr: int = randint(1, 6)
    bot.send_message(message.chat.id, f"если выпадет {pidr}, то ты пидр")
    bot.send_dice(message.chat.id)
    bot.send_message(message.chat.id, "ты можешь отправить мне фото и я тебе его откоментирую(придумал супер полезную функцию)")

@bot.message_handler(func = lambda message: message.text == 'Report a bug')
def helpinf(message):
    bot.send_message(message.chat.id, "<b>Contact support and send this log.</b> """
                                                "@andrkrsv", parse_mode='html')
    bot.send_message(message.chat.id, message)

@bot.message_handler(content_types=['photo'])
def photoreact(message):
    bot.reply_to(message, 'какое охуенное фото, выебать бы кнш', reply_markup=markup)

@bot.message_handler(func = lambda message: message.text == 'Login')
def login(message):
    bot.send_message(message.chat.id, '<b>Выберите способ авторизации:</b>', parse_mode='html', reply_markup=markup3)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'another_auth_method':
        bot.send_message(callback.message.chat.id, '<b>Выберите способ авторизации:</b>', parse_mode='html',reply_markup=markup3)
    elif callback.data == 'no_auth':
        bot.send_message(callback.message.chat.id, '<b>Успешная авторизация.</b>', parse_mode= 'html',
                         reply_markup=markup4)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'github_auth':
        bot.send_message(callback.message.chat.id, 'Перейдите по ссылке и войдите в свой аккаунт GitHub. (ТУТ ДОЛЖНА БЫТЬ ССЫЛКА ИЛИ ЗАПРОС К АПИ)', parse_mode='HTML',reply_markup=markup5)
    elif callback.data == 'telelogin':
        bot.send_message(callback.message.chat.id, 'Запрос Telegram_API')
        bot.send_message(callback.message.chat.id, '<b>Успешная авторизация.</b>', parse_mode='html',
                         reply_markup=markup4)
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.delete_message(callback.message.chat.id, callback.message.message_id + 1)
    elif callback.data == 'khui':
        bot.send_message(callback.message.chat.id,'''❤️❤️❤️❤️❤️❤️❤️
❤️❤️❤️❤️❤️❤️❤️
❤️❤️❤️❤️❤️❤️❤️
❤️❤️❤️❤️❤️❤️❤️
❤️❤️❤️❤️❤️❤️❤️''', reply_markup=markup4)




bot.polling(none_stop=True)
