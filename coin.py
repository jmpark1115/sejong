import requests

def coin_info(**coin):
    coin_type = coin['coin_name']
    url = "https://api.bithumb.com/public/ticker/ALL"

    resp = requests.get(url)
    content = resp.json()

    try:
        if coin_type :
            val = content['data'][coin_type]['closing_price']
            coin_val = "{}({})".format(coin_type, val)
        else:
            BTC = content['data']['BTC']['closing_price']
            ETH = content['data']['ETH']['closing_price']
            BCH = content['data']['BCH']['closing_price']
            XRP = content['data']['XRP']['closing_price']
            coin_val = "BTC({}) ETH({}) BCH({}) XRP({})".format(BTC, ETH, BCH, XRP)
    except:
        coin_val = 'Error'
    return coin_val


# if __name__ == '__main__':
#     print(coin_val())