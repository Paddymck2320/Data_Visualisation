from flask import Flask, render_template, request
import json

from part1 import get_clean_tweets
from part2 import get_polarity

app = Flask(__name__)


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

    df = get_clean_tweets('VAR')

    pos, neg, nue = get_polarity(df)

    labels = ['positive', 'negative', 'neutral']
    values = [pos, neg, nue]

    data = zip(labels, values)

    list = []

    for label, value in data:
        list.append({'name': label, 'y': value})

    return render_template('chart.html', title=title, description_text=desc, chart_name='Pie', data=list)


if __name__ == '__main__':
    app.run()
