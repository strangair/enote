#!/usr/bin/python
# coding: utf-8

from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def xyu(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Пизда!")	

def record(bot, update):
	f = open('test.tmp', 'w')
	message = update.message.text
	message = message.split(' ', 1)[1]	
	f.write(message)

	f.close()

def digest(bot, update):
	f = open('test.tmp', 'r')

#	if args == False:
	bot.sendMessage(chat_id=update.message.chat_id, text=f.readline())
	f.close()

updater = Updater(token='283098184:AAEztJC92M9wczX0WyXd1vuHuF7uM3ObeuU')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

dispatcher.add_handler(CommandHandler('хуй', xyu))
dispatcher.add_handler(CommandHandler('пиши', record))
dispatcher.add_handler(CommandHandler('чокаво', digest))

updater.start_polling()

updater.idle()


