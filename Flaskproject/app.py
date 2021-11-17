from flask import Flask, render_template, request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import tweepy as tp
import pandas as pd
import json
import re
from matplotlib import pyplot as plt
from twitter_auth import *

app = Flask(__name__)

auth = tp.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tp.API(auth)

def clean_tweet(input):
    return re.sub('[^A-Za-z0-9 ]+','', input)

def get_clean_tweets(query='brexit'):

    tweets = {}

    vdr = SentimentIntensityAnalyzer()

    tweets_from_api = api.search(q=query)

    id = 0

    for tweet in tweets_from_api:
        tweets[id] = {
            'id':id,
            'username':tweet.user.name,
            'text': clean_tweet(tweet.text),
            'sentiment': vdr.polarity_scores(tweet.text)['compound']
        }
        id+=1

    df = pd.DataFrame.from_dict(tweets, orient='index')

    df.set_index('id', inplace=True)

    df.to_csv('static/CSV/output.csv')

    return df

def get_polarity(tweets):
    return (tweets['sentiment']> .25).sum(), (tweets['sentiment']< -.25).sum(), (tweets['sentiment'].between(-.25, .25)).sum()

def display_graph(p, n , neu):
    labels = ['postitive', 'negative', 'neutral']
    values = [p,n,neu]

    plt.title('Sentiment Analysis')

    plt.pie(values, labels=labels, autopct='%1.1f%%')

    plt.show()


if __name__ == '__main__':
    df = pd.read_csv('static/CSV/output.csv')

    df.set_index('id', inplace=True)

    postitive, negative, neutral = get_polarity(df)

    display_graph(postitive, negative, neutral)


@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/about', methods=['GET'])
def aboutpage():
    return render_template('about.html')

@app.route('/chart')
def display_graph():  # put application's code here
    title = 'Data Vis Project 2021'
    desc = 'A chart to viualise sentiment'

    df = get_clean_tweets('brexit')

    pos, neg, nue = get_polarity(df)

    labels = ['positive', 'negative', 'neutral']
    values = [pos, neg, nue]

    data = zip(labels, values)

    list = []

    for label, value in data:
        list.append({'name':label, 'y': value})


    return render_template('chart.html', title=title,description_text=desc, chart_name='Pie', data=list)

@app.route('/tweets', methods=['POST'])
def tweetspage():  # put application's code here

    if request.method == 'POST':
        query = request.form['query']
        tweets = api.search(query)

        return render_template('results.html', query=tweets)

    return render_template('404.html')



if __name__ == '__main__':
    app.run()
