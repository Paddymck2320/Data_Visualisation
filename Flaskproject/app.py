from flask import Flask, render_template, request
import json

from part1 import get_clean_tweets
from part1 import get_clean_tweets1
from part2 import get_polarity
from part2 import get_polarity1

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/about', methods=['GET'])


@app.route('/chart')
def display_graph():  # put application's code here
    title = 'Data Vis Project 2021'
    desc = 'A chart to viualise sentiment'

    df = get_clean_tweets()
    pos, neg, nue = get_polarity(df)

    labels = ['positive', 'negative', 'neutral']
    values = [pos, neg, nue]

    data = zip(labels, values)

    list = []

    for label, value in data:
        list.append({'name': label, 'y': value})

    title1 = 'Data Vis Project 2021'
    desc1 = 'A chart to viualise sentiment'

    df1 = get_clean_tweets1()

    pos1, neg1, nue1 = get_polarity1(df1)

    labels1 = ['positive', 'negative', 'neutral']
    values1 = [pos1, neg1, nue1]

    data1 = zip(labels1, values1)

    list1 = []

    for label1, value1 in data1:
        list1.append({'name': label1, 'y': value1})

    return render_template('chart.html', title=title, title1=title1, description_text=desc, description_text1=desc1, chart_name='Pie', chart_name1='Pie', data=list, data1=list1)


if __name__ == '__main__':
    app.run()
