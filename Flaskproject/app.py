from flask import Flask, render_template, request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import tweepy as tp
import pandas as pd
import json
from twitter_auth import *

auth = tp.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tp.API(auth)

app = Flask(__name__)


tweets = api.search(q='brexit')

list = []

for tweet in tweets:

    sentiment = TextBlob(tweet.text).sentiment.polarity

    if sentiment > 0.15:
        sentiment = 'positive'
    elif sentiment < -.15:
        sentiment = 'neg'
    else:
        sentiment = 'neu'

    list.append((tweet.text, sentiment))

df = pd.DataFrame(list)

df.to_csv("static/CSV/output.csv", sep=",")

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/about', methods=['GET'])
def aboutpage():
    return render_template('about.html')

@app.route('/chart')
def chart():
    df = pd.read_csv('static/CSV/output.csv', header=None)
    series = {}
    drilldown = {}

    series['name'] = 'Tweets'
    series['colorByPoint'] = 'true'

    drilldown['series'] = []
    current_value = None
    data = []
    series_data = []
    value = 0

    for row in df.iterrows():

        ent = row[1]

        id = ent[0]
        cat = ent[1]
        val = ent[2]

        if current_value == None:
            current_value = id

        if id != current_value:
            list_item = {}
            series_list_item = {}

            list_item['name'] = current_value
            list_item['id'] = current_value
            list_item['data'] = data

            series_list_item['name'] = current_value
            series_list_item['y'] = value
            series_list_item['drilldown'] = current_value

            series_data.append(series_list_item)

            data = []
            value = 0
            drilldown['series'].append(list_item)
            current_value = id

        data.append([id, val])
        value += id

    list_item = {}
    series_list_item = {}

    list_item['name'] = current_value
    list_item['id'] = current_value
    list_item['data'] = data

    series_list_item["name"] = current_value
    series_list_item["y"] = value
    series_list_item["drilldown"] = current_value

    series_data.append(series_list_item)

    data = []
    value = 0
    drilldown['series'].append(list_item)

    series['data'] = series_data

    series = json.dumps(series)
    drilldown = json.dumps(drilldown)

    print(drilldown)
    print(series)
    return render_template('chart.html', series=series, drilldown = drilldown)


@app.route('/tweets', methods=['POST'])
def tweetspage():  # put application's code here

    if request.method == 'POST':
        query = request.form['query']
        tweets = api.search(query)

        return render_template('results.html', query=tweets)

    return render_template('404.html')


if __name__ == '__main__':
    app.run()
