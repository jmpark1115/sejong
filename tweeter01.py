import requests
from requests_oauthlib import OAuth1
from configparser import ConfigParser

config = ConfigParser()
config.read('crawl.conf')

consumer_key = config.get('Twitter', 'consumer_key')
consumer_secret = config.get('Twitter', 'consumer_secret')
access_token = config.get('Twitter', 'access_token')
access_token_secret = config.get('Twitter', 'access_token_secret')

oauth = OAuth1(client_key=consumer_key, client_secret=consumer_secret,
               resource_owner_key=access_token, resource_owner_secret=access_token_secret)
# Twitter REST api // screen_name 은 트위터 계정명
url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={0}' .format('realdonaldtrump')
    # .format('justinsuntron')

r = requests.get(url=url, auth=oauth)
statuses =  r.json()


cnt = 0
for status in statuses:
    print('[%d] :' % cnt)
    print(status['created_at'])
    print(status['text'])

"""
cnt = 0
for status in statuses:
    if 'cave' in status['text']:
        cnt += 1
        print('[%d] :' % cnt)
        print(status['created_at'])
        print(status['text'])
"""