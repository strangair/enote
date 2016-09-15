#!/usr/bin/python
# coding: utf-8

from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
import logging
import json
from datetime import datetime, timedelta
from uuid import uuid4

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

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

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
	/морква         Морква
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

def sausage(bot, update):
    bot.sendDocument(chat_id=update.message.chat_id, document='https://media.giphy.com/media/JVqeFxl3Qo8/giphy.gif')


def carrot(bot, update):
    bot.sendDocument(chat_id=update.message.chat_id, document='http://i.imgur.com/KwxaJWq.gif')

def inlinequery(bot, update):
    query = update.inline_query.query
    results = list()

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title="тест",
                                            input_message_content=InputTextMessageContent))

    bot.answerInlineQuery(update.inline_query.id, results=results)

def main():
    updater = Updater(token='283098184:AAEztJC92M9wczX0WyXd1vuHuF7uM3ObeuU')

    dp = updater.dispatcher

    # Add commands
    dp.add_handler(CommandHandler('хуй', xyu))
    dp.add_handler(CommandHandler('пиши', record))
    dp.add_handler(CommandHandler('чокаво', digest))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('сосисочки', sausage))
    dp.add_handler(CommandHandler('морква', carrot))

    dp.add_handler(InlineQueryHandler(inlinequery))

    dp.add_error_handler(info)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()