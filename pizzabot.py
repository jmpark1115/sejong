# -*- coding: utf-8 -*-

import requests
import json
import urllib.request
from configparser import ConfigParser, NoSectionError
from PIL import Image
from weather import weather_info
from coin    import coin_val

from flask import Flask, request, jsonify, render_template

ERROR_MESSAGE = '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.'
URL_OPEN_TIME_OUT = 10

import os

config = ConfigParser()
try:
    # script relative path
    ab = os.path.dirname(__file__)
    config.read(os.path.join(ab, 'quizbot.conf'))
    MODE = config.get('ENV', 'MODE')
    BASE_URL = config.get(MODE, 'BASE_URL')
    TOKEN = config.get(MODE, 'TOKEN')
    WEBHOOK = config.get(MODE, 'PATH')
    DEBUG_MODE = config.get(MODE, 'DEBUG_MODE')
    print(MODE, BASE_URL, TOKEN, WEBHOOK, DEBUG_MODE)
except NoSectionError:
    print("========>>> NoSectionError")


app = Flask(__name__)

# ----------------------------------------------------
# 사진 구함
# ----------------------------------------------------
def get_photo(answer):
    photo = ''
    index = answer.find('</Photo>')

    if index >= 0:
        photo = answer[len('<Photo>'):index]
        answer = answer[index + len('</Photo>'):]

    return answer, photo


# ----------------------------------------------------
# 사진 크기 구함
# ----------------------------------------------------
def get_photo_size(url):

    width = 0
    height = 0

    if url == '':
        return width, height

    try:
        file = urllib.request.urlopen(url, timeout=URL_OPEN_TIME_OUT)
        img = Image.open(file)
        width, height = img.size
    except:
        print("photo size error!")

    print("width, heigth %s %s" % (width, height))
    return width, height

# ----------------------------------------------------
# 메뉴 구함
# ----------------------------------------------------
def get_menu(answer):
    # --------------------------------
    # 메뉴가 있는지 검사
    # --------------------------------
    menu = []
    index = answer.find(' 1. ')

    if index < 0:
        return answer, menu

    menu_string = answer[index + 1:]
    answer = answer[:index]

    # --------------------------------
    # 메뉴를 배열로 설정
    # --------------------------------
    number = 1

    while 1:
        number += 1
        search_string = ' %d. ' % number
        index = menu_string.find(search_string)

        if index < 0:
            menu.append(menu_string[3:].strip())
            break

        menu.append(menu_string[3:index].strip())
        menu_string = menu_string[index + 1:]

    return answer, menu


# ----------------------------------------------------
# 메뉴 버튼 구함
# ----------------------------------------------------
def get_menu_button(menu):
    if len(menu) == 0:
        return None

    menu_button = {
        'type': 'buttons',
        'buttons': menu
    }

    return menu_button


# ----------------------------------------------------
# Dialogflow에서 대답 구함
# ----------------------------------------------------
def get_answer(text, user_key):
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
        return ERROR_MESSAGE

    data_receive = res.json()
    answer = data_receive['result']['fulfillment']['speech']

    return answer

# ----------------------------------------------------
# 피자 정보 처리
# ----------------------------------------------------

def pizza_info(**pizza):
    pizza_name = pizza['pizza_type']
    answer = ""
    if pizza_name == u'불고기피자':
        answer = '<Photo>http://{}/quizbot/static/bulgogi.jpg</Photo>'.format(BASE_URL)
        answer += '한국의 맛 불고기를 부드러운 치즈와 함께!'
    elif pizza_name == u'페퍼로니피자':
        answer = '<Photo>http://{}/quizbot/static/peperroni.jpg</Photo>'.format(BASE_URL)
        answer += '고소한 페파로니햄이 쫀득한 치즈위로 뜸뿍!'
    elif pizza_name == u'포테이토피자':
        answer = '<Photo>http://{}/quizbot/static/potato.jpg</Photo>'.format(BASE_URL)
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
@app.route("/webhook", methods=['POST'])
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
    return jsonify(res)

# ----------------------------------------------------
# 카카오톡 키보드 처리
# ----------------------------------------------------
@app.route("/keyboard")
def keyboard():
    res = {
        'type': 'buttons',
        'buttons': ['대화하기']
    }

    return jsonify(res)


# ----------------------------------------------------
# 카카오톡 메시지 처리
# ----------------------------------------------------
@app.route('/message', methods=['POST'])
def message():
    # --------------------------------
    # 메시지 받기
    # --------------------------------
    req = request.get_json()
    user_key = req['user_key']
    content = req['content']

    print("user_key: {}, content: {}" .format(user_key, content))
    if len(user_key) <= 0 or len(content) <= 0:
        answer = ERROR_MESSAGE

    # --------------------------------
    # 답변 구함
    # --------------------------------

    if content == u'안녕':
        answer = '안녕하세요! 좋은 하루되세요'
    elif content == u'대화하기':
        answer = '안녕하세요! 전 피자 주문을 받는 챗봇입니다~'
    else:
        answer = get_answer(content, user_key)

    # --------------------------------
    # 사진 구함
    # --------------------------------
    answer, photo = get_photo(answer)
    photo_width, photo_height = get_photo_size(photo)

    # --------------------------------
    # 메뉴 구함
    # --------------------------------
    answer, menu = get_menu(answer)

    # --------------------------------
    # 메시지 설정
    # --------------------------------
    res = {
        'message': {
            'text': answer
        }
    }

    # --------------------------------
    # 사진 설정
    # --------------------------------
    if photo != '' and photo_width > 0 and photo_height > 0:
        res['message']['photo'] = {
            'url':  photo,
            'width': photo_width,
            'height': photo_height
        }

    # --------------------------------
    # 메뉴 버튼 설정
    # --------------------------------
    menu_button = get_menu_button(menu)

    if menu_button != None:
        res['keyboard'] = menu_button

    return jsonify(res)

@app.route('/')
def index():
    return '<h1>welcome to chatbot world</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s' %name

@app.route('/ex01')
def ex01():
    return render_template('ex01.html')
# ----------------------------------------------------
# 메인 함수
# ----------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True, debug=DEBUG_MODE)
