#!/usr/bin/python
# coding: utf-8

from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
import json

from datetime import datetime, timedelta

# Set encoding
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Global block
chat_history = 'chat_history.txt'
today = datetime.now()
today = today.strftime("%Y-%m-%d")
yesterday = datetime.now() - timedelta(days=1)
yesterday = yesterday.strftime("%Y-%m-%d")

def xyu(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Пизда!")	

def record(bot, update):
    f = open(chat_history, 'w')

    message = update.message.text
    message = message.split(' ', 1)[1]

    data = {
        'date': today,
        'text': message
    }

    # Convert to JSON & append to the file
    f = open(chat_history, 'a+')
    f.write(json.dumps(data, ensure_ascii=False, encoding="utf-8") + '\n')
    f.close()


def digest(bot, update, **args):
    with open(chat_history) as f:
        for line in f:
            data = json.loads(line)
            if args[0] == 'вчера':
                if data['date'] == yesterday:
                    bot.sendMessage(chat_id=update.message.chat_id, text=data['text'])
            else:
                if data['date'] == today:
                    bot.sendMessage(chat_id=update.message.chat_id, text=data['text'])

updater = Updater(token='283098184:AAEztJC92M9wczX0WyXd1vuHuF7uM3ObeuU')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

dispatcher.add_handler(CommandHandler('хуй', xyu))
dispatcher.add_handler(CommandHandler('пиши', record))
dispatcher.add_handler(CommandHandler('чокаво', digest))

updater.start_polling()

updater.idle()


