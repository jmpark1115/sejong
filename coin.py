import requests, json

def coin_val():
    url = "https://api.bithumb.com/public/ticker/ALL"

    resp = requests.get(url)
    content = json.loads(resp.content)
    BTC = content['data']['BTC']['closing_price']
    ETH = content['data']['ETH']['closing_price']
    BCH = content['data']['BCH']['closing_price']
    XRP = content['data']['XRP']['closing_price']
    return BTC, ETH, BCH, XRP

"""
url = "https://api.coinone.co.kr/ticker"
payload = {'currency':'btc'}
resp = requests.get(url, params=payload)
content = resp.json() #json.loads(resp.content)
print(content)
"""

if __name__ == '__main__':
    print(coin_val())