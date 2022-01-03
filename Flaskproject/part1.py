from twitter_auth import *
import tweepy as tp
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd


def clean_tweet(input):
    return re.sub('[^A-Za-z0-9 ]+', '', input)


def get_clean_tweets():
    auth = tp.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tp.API(auth)

    tweets = {}

    vdr = SentimentIntensityAnalyzer()

    tweets_from_api = tp.Cursor(api.search_tweets, q="VAR", lang="en").items(50)

    id = 0

    for tweet in tweets_from_api:
        tweets[id] = {
            'id': id,
            'username': tweet.user.name,
            'location': tweet.user.location,
            'text': clean_tweet(tweet.text),
            'sentiment': vdr.polarity_scores(tweet.text)['compound']
        }
        id += 1

    df = pd.DataFrame.from_dict(tweets, orient='index')

    df.set_index('id', inplace=True)

    df.to_csv('output.csv', mode='a', header=False)

    return df

def get_clean_tweets1():
    auth1 = tp.OAuthHandler(API_KEY, API_SECRET)
    auth1.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tp.API(auth1)

    tweets1 = {}

    vdr = SentimentIntensityAnalyzer()

    tweets_from_api = tp.Cursor(api.search_tweets, q="Vaccine", lang="en").items(50)

    id = 0

    for tweet in tweets_from_api:
        tweets1[id] = {
            'id': id,
            'username': tweet.user.name,
            'location': tweet.user.location,
            'text': clean_tweet(tweet.text),
            'sentiment': vdr.polarity_scores(tweet.text)['compound']
        }
        id += 1

    df1 = pd.DataFrame.from_dict(tweets1, orient='index')

    df1.set_index('id', inplace=True)

    df1.to_csv('output1.csv', mode='a', header=False)

    return df1

if __name__ == '__main__':
    get_clean_tweets()
    get_clean_tweets1()
