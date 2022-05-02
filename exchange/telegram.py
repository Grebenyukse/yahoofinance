# token = 5364460446:AAGxpCglqUunPCyEU5ziIMvHOtSedT9Cp_k
# username = grebenyukSignalsBot
# name = grebenyukSignals
# https://api.telegram.org/bot5364460446:AAGxpCglqUunPCyEU5ziIMvHOtSedT9Cp_k/getUpdates

import requests


def send_alert(message):
    token = '5364460446:AAGxpCglqUunPCyEU5ziIMvHOtSedT9Cp_k'
    chat_id = '253052558'
    url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + 'parseMode=MarkdownV2&text=' + message
    response = requests.get(url)
    return response.json()

