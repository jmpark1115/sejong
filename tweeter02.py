import tweepy
import json

from configparser import ConfigParser

config = ConfigParser()
config.read('crawl.conf')

consumer_key = config.get('Twitter', 'consumer_key')
consumer_secret = config.get('Twitter', 'consumer_secret')
access_token = config.get('Twitter', 'access_token')
access_token_secret = config.get('Twitter', 'access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

keyword = "노트르담"
result = []

for i in range(0,2):
    tweets = api.search(keyword)
    for tweet in tweets:
        result.append([tweet.id_str, tweet.text, str(tweet.created_at)])
        print('-----------')
        print(tweet.id_str)
        print(tweet.created_at)
        print(tweet.text)
        print('\n')

print(result)

file = 'twitter.txt'

try:
    with open(file, mode='w+') as f:
        json.dump(result, f)
except Exception as ex:
    print("except processed", ex)
