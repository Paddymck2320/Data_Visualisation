from twitter_auth import *
import tweepy as tp
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from csv import writer


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

    return tweets

def append_list_as_row(file_name, tweet, vdr):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(tweet)
    row_contents = [id, tweet.user.name, tweet.user.location, clean_tweet(tweet.text),
                    vdr.polarity_scores(tweet.text)['compound']]
    append_list_as_row('output.csv', row_contents)



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


def append_list_as_row(file_name, tweet, vdr):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(tweet)
    row_contents = [id, tweet.user.name, tweet.user.location, clean_tweet(tweet.text),
                    vdr.polarity_scores(tweet.text)['compound']]
    append_list_as_row('output1.csv', row_contents)


if __name__ == '__main__':
    get_clean_tweets()
    get_clean_tweets1()
