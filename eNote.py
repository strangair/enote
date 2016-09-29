#!/usr/bin/python
# coding: utf-8

from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
import logging
import json
import daemon, time
from datetime import datetime, timedelta
from uuid import uuid4
import getopt
import vk
import httplib

# Set encoding
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Global block
chat_history = '/home/ec2-user/enote/chat_history.txt'
log_file = '/home/ec2-user/enote/enote.log'

today = datetime.now()
today = today.strftime("%Y-%m-%d")

# Set logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def xyu(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Пизда!")	

def help(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="""
	Command list:
	/хуй                                    Пизда
	/help                                   Это сообщение
	/запомни <text>                         Запись текста в буфер
	/чокаво <вчера>/<неделя>/<месяц>        Чтение текста из буфера
	/вконтач <n>                            N последних записей из Охотников Апокалипсиса
	/сосисочки                              Сосисочки
	/морква                                 Морква
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
    command = update.message.text
    try:
        command = command.split(' ', 1)[1]
        command = command.split(' ', 1)[0]
    except IndexError:
        command = 'сегодня'

    with open(chat_history) as f:
        for line in f:
            data = json.loads(line)
            datestamp = datetime.date(datetime.strptime(data['date'], "%Y-%m-%d"))

            if command == 'вчера':
                if datestamp > datetime.date((datetime.now() - timedelta(days=1))):
                    bot.sendMessage(chat_id=update.message.chat_id, text=data['text'])
            elif command == 'неделя':
                if datestamp > datetime.date((datetime.now() - timedelta(days=7))):
                    bot.sendMessage(chat_id=update.message.chat_id, text=data['text'])
            elif command == 'месяц':
                if datestamp > datetime.date((datetime.now() - timedelta(days=31))):
                    bot.sendMessage(chat_id=update.message.chat_id, text=data['text'])
            else:
                if datestamp == datetime.date(datetime.now()):
                    bot.sendMessage(chat_id=update.message.chat_id, text=data['text'])

def sausage(bot, update):
    bot.sendDocument(chat_id=update.message.chat_id, document='https://media.giphy.com/media/JVqeFxl3Qo8/giphy.gif')

def carrot(bot, update):
    bot.sendDocument(chat_id=update.message.chat_id, document='http://i.imgur.com/KwxaJWq.gif')

def vkontakte(bot, update):

    count = update.message.text
    try:
        count = count.split(' ', 1)[1]
        count = int(count.split(' ', 1)[0])
    except IndexError:
        count = 1

    if count > 20:
        count = 20

    session = vk.AuthSession(app_id='5645196')
    api = vk.API(session)
    rec = api.wall.get(domain='apocalypse_hunters', count=count)

    for x in range(1, len(rec)):
        message = datetime.fromtimestamp(rec[x]['date']).strftime('%H:%M:%S %Y-%m-%d') + '\n' + \
            rec[x]['attachments'][0]['link']['title'] + '\n' + rec[x]['attachments'][0]['link']['url']
        bot.sendMessage(chat_id=update.message.chat_id, text=message)

def instagram (bot, update):
    command = update.message.text
    try:
        command = command.split(' ', 1)[1]
        command = command.split(' ', 1)[0]
    except IndexError:
        bot.sendMessage(chat_id=update.message.chat_id, text="No username specified")
        break

    url = "/" + command + "/media/"
    # https: // www.instagram.com / varnavsky / media /
    conn = httplib.HTTPSConnection("www.instagram.com")
    conn.request("GET", url)
    res = conn.getresponse()

    data = json.loads(res.read())
    bot.sendMessage(chat_id=update.message.chat_id, text=data['items'][0]['link'])

def inlinequery(bot, update):
    query = update.inline_query.query
    results = list()

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title="test",
                                            input_message_content=InputTextMessageContent))

    bot.answerInlineQuery(update.inline_query.id, results=results)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():

    updater = Updater(token='283098184:AAEztJC92M9wczX0WyXd1vuHuF7uM3ObeuU')

    dp = updater.dispatcher

    # Add commands
    dp.add_handler(CommandHandler('хуй', xyu))
    dp.add_handler(CommandHandler('запомни', record))
    dp.add_handler(CommandHandler('чокаво', digest))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('сосисочки', sausage))
    dp.add_handler(CommandHandler('морква', carrot))
    dp.add_handler(CommandHandler('вконтач', vkontakte))
    dp.add_handler(CommandHandler('инста', instagram))

    dp.add_handler(InlineQueryHandler(inlinequery))

    logger.addHandler(logging.FileHandler(log_file))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "-hd", ["help", "daemon"])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    mode = "foreground"
    for o, a in opts:
        if o in ("-d", "--daemon"):
            mode = "daemon"

    if mode == "daemon":
        with daemon.DaemonContext(
                files_preserve=[
                    logging.FileHandler(log_file),
                ]
        ):
            main()
    else:
        main()