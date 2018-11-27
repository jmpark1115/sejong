from flask import Flask, request, jsonify
from coin import coin_val
import json

mylist1 = ['코인', '날씨', '번역']
mylist2 = ['죽전동', '강남역', '처음으로']

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/keyboard", methods = ['GET'])
def keyboard():
    message = {
        'type':'buttons',
        'buttons' : mylist1
    }
    return jsonify(message)

@app.route("/message", methods = ['POST'])
def message():
    resp = request.get_json()
    content = resp['content']
    
    if content == '코인':
        print('=>코인')
        BTC, ETH,BCH,XRP = coin_val()
        message = {
            'message':{
                'text': 'BTC({}) ETH({}) BCH({}) XRP({} by bithumb' 
                .format(BTC, ETH, BCH, XRP)
            },
            'keyboard':{
                'type' : 'buttons',
                'buttons' : mylist1
            }
        }
        
    elif content == '날씨':
        print('날씨')
        message = {
            'message': {
                'text':'날씨를 선택하세요'
            },
            'keyboard':{
                'type':'buttons',
                'buttons': mylist2
            }
        }
    
    elif content.find('강남역') != -1:
        print('강남역 날씨')
        msg = '강남역 날씨 맑음 5도'
        message = {
            'message': {
                'text' : msg
            },
            'keyboard':{
                'type':'buttons',
                'buttons':mylist2
            }
        }
    elif content.find('죽전동') != -1:
        print('죽전동 날씨')
        msg = '죽전동 날씨 흐림 -5도'
        message = {
            'message': {
                'text' : msg
            },
            'keyboard':{
                'type':'buttons',
                'buttons':mylist2
            }
        }
    
    elif content.find('번역') != -1:
        print('번역')
        msg = '구현 예정입니다'
        message = {
            'message': {
                'text' : msg
            },
            'keyboard':{
                'type':'buttons',
                'buttons':mylist2
            }
        }
        
    elif content == '처음으로':
        print('처음으로')        
        message = {
            'message': {
                'text' : '처음으로 이동합니다'
            },
            'keyboard':{
                'type':'buttons',
                'buttons':mylist1
            }
        }
    else:
        message = {
            'message': {
                'text': '잘못된 입력입니다'
            },
            'keyboard': {
                'type':'buttons',
                'buttons' : mylist1
            }
        }
     
    return jsonify(message)

            
        

if __name__ == '__main__':
    print("run")
    app.run(debug = True, host='0.0.0.0', port=80)