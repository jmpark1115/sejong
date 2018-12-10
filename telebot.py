# coding=utf8

import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules

import time
import datetime
from weather import weather_info
from coin import coin_info
import os
from configparser import ConfigParser, NoSectionError

print('start telegram chat bot')

config = ConfigParser()
try:
    # script relative path
    ab = os.path.dirname(__file__)
    config.read(os.path.join(ab, 'quizbot.conf'))
    MODE = config.get('ENV', 'MODE')
    my_token = config.get('ENV', 'TELEGRAM_TOKEN')
    chief_id = config.get('ENV', 'TELEGRAM_ID')
except NoSectionError:
    print("========>>> NoSectionError")

# 봇 선언
bot = telegram.Bot(token=my_token)

# 커스텀 키보드 설정
custom_keyboard = [
    ["/help", "취소"],
    ["코인", "날씨", "아이디"],
]

custom_keyboard2 = [
    ["/help", "취소"],
    ["죽전동", "강남역", "처음으로"],
]

reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
reply_markup2 = telegram.ReplyKeyboardMarkup(custom_keyboard2, resize_keyboard=True)

# chat_id 아이디 설정
try:
    updates = bot.getUpdates()
    chat_id = updates[-1].message.chat.id
except IndexError:
    chat_id = chief_id

# 커스텀 키보드 설정
bot.send_message(chat_id=chat_id, text="마이챗봇, 커스텀 키보드 설정완료!", reply_markup=reply_markup)

# 시간설정
n = time.localtime().tm_wday
now = datetime.datetime.now()


def hello(bot, update):
    update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))


# help reply function
def help_command(bot, update):
    print("help_command")
    update.message.reply_text("마이챗봇 도움말")
    update.message.reply_text(
        "/help : 명령어 \n 시간 : 현재 시간 \n 코인 : 가상화폐 정보\n 날씨: 지역날씨\n 미세먼지\n 날짜 : 현재 날짜\n id : 당신의 챗 id ")


def start_command(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="안녕하세요!", reply_markup=reply_markup)

    # message reply function


def get_message(bot, update):

    if "코인" in update.message.text:
        print(update.message.text)
        param = {'coin_name': ''}
        coin_val = coin_info(**param)
        update.message.reply_text("%s" % coin_val, reply_markup=reply_markup)

    if "날씨" in update.message.text:
        print(update.message.text)
        update.message.reply_text("날씨", reply_markup=reply_markup2)

    if "죽전동" in update.message.text or "강남역" in update.message.text:
        print(update.message.text)
        params = {'area': update.message.text}
        msg = weather_info(**params)
        update.message.reply_text("%s" % msg, reply_markup=reply_markup2)

        # 날짜와 시간
    if update.message.text == "날짜":
        print(update.message.text)
        now = datetime.datetime.now()
        update.message.reply_text("오늘의 날짜 : \n%s년 %s월 %s일 입니다." % (now.year, now.month, now.day))

    if update.message.text == "시간":
        print(update.message.text)
        now = datetime.datetime.now()
        update.message.reply_text("현재 시간 : \n%s시 %s분 %s초 입니다." % (now.hour, now.minute, now.second))

    if update.message.text == "아이디":
        chat_id = update.message.chat_id
        update.message.reply_text("당신의 chat_id 는 %s 입니다." % chat_id, reply_markup=reply_markup)

    if update.message.text == "처음으로":
        print(update.message.text)
        update.message.reply_text("처음으로", reply_markup=reply_markup)


updater = Updater(my_token)

message_handler = MessageHandler(Filters.text, get_message)
updater.dispatcher.add_handler(message_handler)

help_handler = CommandHandler('help', help_command)
updater.dispatcher.add_handler(help_handler)

hello_handler = CommandHandler('hello', hello)
updater.dispatcher.add_handler(hello_handler)

start_handler = CommandHandler('start', start_command)
updater.dispatcher.add_handler(start_handler)

updater.start_polling(timeout=3, clean=True)
updater.idle()