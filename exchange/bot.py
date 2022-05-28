import requests
import telebot
from telebot import types # для указание типов

chat_id = '253052558'
chat_token = '5364460446:AAGxpCglqUunPCyEU5ziIMvHOtSedT9Cp_k'
tinka_token = "t.eDmKGfqdXmwDFW9279RZc3xhYLKpuu8IP7HNhMtvU7FgQ4gIu7fAhSArpOyrNGcIImz_aW_qDgcEbryMk34I-Q"

bot = telebot.TeleBot(chat_token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data="BUY" + '/' +str(12), text="BUY/567")
    btn2 = types.InlineKeyboardButton(callback_data="SELL", text="SELL")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот для твоей статьи для habr.com".format(message.from_user), reply_markup=markup)
    

@bot.callback_query_handler(func=lambda call: True)    # Обработчик
def callback_inline_first(message):
    info = message.data
    comand = info.spli("/")[0]
    signal_id = info.split("/")[1]
    print(message)


@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == 'accept'):
        print('open position')
    if(message.text == 'decline'):
        print('decline signal')
    if(message.text == "👋 Поздороваться"):
        bot.send_message(message.chat.id, text="Привеет.. Спасибо что читаешь статью!)")
    elif(message.text == "❓ Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как меня зовут?")
        btn2 = types.KeyboardButton("Что я могу?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
    
    elif(message.text == "Как меня зовут?"):
        bot.send_message(message.chat.id, "У меня нет имени..")
    
    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text="Поздороваться с читателями")
    
    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Поздороваться")
        button2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")

bot.polling(none_stop=True)