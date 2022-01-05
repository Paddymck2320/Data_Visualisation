from twitter_auth import *
import tweepy as tp
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd



def clean_tweet(input):
    return re.sub('[^A-Za-z0-9 ]+', '', input)


def get_clean_tweets(query):
    auth = tp.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tp.API(auth)

    tweets = {}


    vdr = SentimentIntensityAnalyzer()

    tweets_from_api = tp.Cursor(api.search_tweets, q=query, lang="en").items(50)

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

    return tweets_from_api, df


if __name__ == '__main__':
    get_clean_tweets()
