# token = 5364460446:AAGxpCglqUunPCyEU5ziIMvHOtSedT9Cp_k
# username = grebenyukSignalsBot
# name = grebenyukSignals
# https://api.telegram.org/bot5364460446:AAGxpCglqUunPCyEU5ziIMvHOtSedT9Cp_k/getUpdates

import requests
import telebot
from telebot import types

from exchange.config import chat_token, chat_id

bot = telebot.TeleBot(chat_token)


def send_photo(pic, message, signal_id):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data='accept/' + str(signal_id), text="Accept")
    btn2 = types.InlineKeyboardButton(callback_data='decline/' + str(signal_id), text="Decline")
    markup.add(btn1, btn2)
    bot.send_photo(chat_id=chat_id, photo=open(pic, 'rb'), caption=message, reply_markup=markup)