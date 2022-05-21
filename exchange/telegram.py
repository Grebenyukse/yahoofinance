# token = 5364460446:AAGxpCglqUunPCyEU5ziIMvHOtSedT9Cp_k
# username = grebenyukSignalsBot
# name = grebenyukSignals
# https://api.telegram.org/bot5364460446:AAGxpCglqUunPCyEU5ziIMvHOtSedT9Cp_k/getUpdates

import requests
import telebot

chat_id = '253052558'
token = '5364460446:AAGxpCglqUunPCyEU5ziIMvHOtSedT9Cp_k'


def send_alert(message):
    url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + 'parseMode=MarkdownV2&text=' + message
    response = requests.get(url)
    return response.json()


def send_photo(pic, message):
    bot = telebot.TeleBot(token)
    bot.send_photo(chat_id=chat_id, photo=open(pic,'rb'), caption=message)