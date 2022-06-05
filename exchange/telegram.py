import telebot
from telebot import types
from dao.subscribers import fetch_subscribers

from exchange.config import chat_token, chat_id

bot = telebot.TeleBot(chat_token)


def send_photo(pic, message, signal_id):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data='accept/' + str(signal_id), text="Accept")
    btn2 = types.InlineKeyboardButton(callback_data='decline/' + str(signal_id), text="Decline")
    markup.add(btn1, btn2)
    subscriber_ids = fetch_subscribers()
    for id in subscriber_ids:
        bot.send_photo(chat_id=id, photo=open(pic, 'rb'), caption=message, reply_markup=markup)