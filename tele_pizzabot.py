# coding=utf8
#this program is syncronized with dialogflow PizzaBot_dev AND sejongT via Telegram

import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules
from flask import Flask, request, jsonify, render_template

import time
import datetime
import requests
import json
import os
from configparser import ConfigParser, NoSectionError

from coin import coin_info
from weather import weather_info

print('start telegram chat bot')

config = ConfigParser()
try:
    # script relative path
    ab = os.path.dirname(__file__)
    config.read(os.path.join(ab, 'telebot.conf'))
    MODE = config.get('ENV', 'MODE')
    my_token = config.get('ENV', 'TELEGRAM_TOKEN')
    chat_id = config.get('ENV', 'TELEGRAM_ID')
    TOKEN = config.get(MODE, 'TOKEN')
    DEBUG_MODE = config.get(MODE, 'DEBUG_MODE')
    print(MODE, my_token, chat_id, TOKEN)
except NoSectionError:
    print("========>>> NoSectionError")

app = Flask(__name__)


# 커스텀 키보드 설정
custom_keyboard0 = [
    ['/help', '/hello'],
    ['메뉴', '주문'],
]

reply_markup0 = telegram.ReplyKeyboardMarkup(custom_keyboard0, resize_keyboard=True)

def hello(bot, update):
    update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))


# help reply function
def help_command(bot, update):
    update.message.reply_text("마이챗봇 도움말")
    update.message.reply_text(
        "/help : 명령어 \n /hello : 인사 \n 코인 : 가상화폐 정보\n 메뉴 : 피자주문 ")


def start_command(bot, update):
    update.message.reply_text(text="안녕하세요! 시작합니다", reply_markup=reply_markup0)
    

# ----------------------------------------------------
# 사진 체크
# ----------------------------------------------------
def check_photo(answer):

    photo = ''
    index = answer.find('</Photo>')

    if index >= 0:
        photo = answer[len('<Photo>'):index]
        answer = answer[index + len('</Photo>'):]

    return answer, photo

# ----------------------------------------------------
# 피자 정보 처리
# ----------------------------------------------------

def pizza_info(**pizza):

    pizza_name = pizza['pizza_type']
    answer = ""
    if pizza_name == u'불고기피자':
        answer = '<Photo>http://www.pizzamaru.co.kr/UpFile/Menu/cla8_F_01.jpg</Photo>'
        answer += '한국의 맛 불고기를 부드러운 치즈와 함께!'
    elif pizza_name == u'페퍼로니피자':
        answer = '<Photo>http://www.pizzamaru.co.kr/UpFile/Menu/cla6_F_01.jpg</Photo>'
        answer += '고소한 페파로니햄이 쫀득한 치즈위로 뜸뿍!'
    elif pizza_name == u'포테이토피자':
        answer = '<Photo>http://www.pizzamaru.co.kr/UpFile/Menu/cla7_F_01.jpg</Photo>'
        answer += '저칼로리 감자의 담백한 맛!'

    print("pizza_info [%s]" %answer)
    return answer


# ----------------------------------------------------
# 피자 주문 처리
# ----------------------------------------------------
def pizza_order(**order):

    print("pizza_order")
    pizza_name = order['pizza_type']
    address    = order['address']

    answer = pizza_name + '를 주문하셨습니다.\n'
    answer += "[" + address + "]의 주소로 지금 배달하도록 하겠습니다.\n"
    answer += '주문해 주셔서 감사합니다.'

    return answer


# ----------------------------------------------------
# Dialogflow fullfillment 처리
# ----------------------------------------------------
@app.route('/webhook', methods=['POST'])
def webhook():
    # --------------------------------
    # 액션 구함
    # --------------------------------
    req = request.get_json(force=True)
    action_str = req['result']['action']
    params = req['result']['parameters']

    print("action name [%s]" % action_str)
    print("params [%s]" % params)

    action = eval(action_str)

    if callable(action):
        answer = action(**params)
    else:
        answer = 'error'

    res = {'speech':answer}
    return jsonify(res)   #return to dialogflow

# ----------------------------------------------------
# Dialogflow에서 대답 구함
# ----------------------------------------------------
def send_message_dialogflow(text, user_key):
    # --------------------------------
    # Dialogflow에 요청
    # --------------------------------
    data_send = {
        'lang': 'ko',
        'query': text,
        'sessionId': user_key,
        'timezone': 'Asia/Seoul'
    }

    data_header = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + TOKEN  # Dialogflow의 Client access token 입력
    }

    dialogflow_url = 'https://api.dialogflow.com/v1/query?v=20150910'

    res = requests.post(dialogflow_url,
                        data=json.dumps(data_send),
                        headers=data_header)

    # --------------------------------
    # 대답 처리
    # --------------------------------
    if res.status_code != requests.codes.ok:
        return '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.'

    data_receive = res.json()
    answer = data_receive['result']['fulfillment']['speech']

    return answer

def get_message(bot, update):

    print(update.message.text)
    content = update.message.text
    chat_id = update.message.chat_id
    dialog_answer = send_message_dialogflow(content, chat_id)
    # --------------------------------
    # 사진이 있다면 이미지를 처리함
    # --------------------------------
    answer, photo = check_photo(dialog_answer)
    update.message.reply_text("%s" % answer, reply_markup = reply_markup0)
    if photo:
        update.message.reply_photo(photo)


@app.route('/')
def index():
    return '<h1>welcome to chatbot world</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s' %name

@app.route('/ex01')
def ex01():
    return render_template('ex01.html')


def main():
    updater = Updater(my_token)
    updater.bot.send_message(chat_id = chat_id,
                             text="마이챗봇에 오신 것을 환영합니다",
                             reply_markup = reply_markup0)

    message_handler = MessageHandler(Filters.text, get_message)
    updater.dispatcher.add_handler(message_handler)

    help_handler = CommandHandler('help', help_command)
    updater.dispatcher.add_handler(help_handler)

    hello_handler = CommandHandler('hello', hello)
    updater.dispatcher.add_handler(hello_handler)

    start_handler = CommandHandler('start', start_command)
    updater.dispatcher.add_handler(start_handler)

    updater.start_polling(timeout=3, clean=True)
    # updater.idle()

if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0', port=80, threaded=True, debug=DEBUG_MODE)
    print('Program aborted')