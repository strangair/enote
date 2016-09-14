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

def help(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="""
	Command list:
	/хуй            Пизда
	/help           Это сообщение
	/пиши <text>    Запись текста в буфер
	/чокаво         Чтение текста из буфера
	/сосисочки      Сосисочки
	""")

def record(bot, update):

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

def digest(bot, update):
    with open(chat_history) as f:
        for line in f:
            data = json.loads(line)

            if data['date'] == today:
                bot.sendMessage(chat_id=update.message.chat_id, text=data['text'])

def sausages(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=upload_photo)
    bot.sendDocument(chat_id=update.message.chat_id, document='https://media.giphy.com/media/JVqeFxl3Qo8/giphy.gif')

def main():
    updater = Updater(token='283098184:AAEztJC92M9wczX0WyXd1vuHuF7uM3ObeuU')

    dp = updater.dispatcher

    # Add commands
    dp.add_handler(CommandHandler('хуй', xyu))
    dp.add_handler(CommandHandler('пиши', record))
    dp.add_handler(CommandHandler('чокаво', digest))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('сосисочки', sausages))

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()