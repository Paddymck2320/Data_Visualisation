from flask import Flask, render_template, request
import json

from part1 import get_clean_tweets
import part2 as part2

app = Flask(__name__)




@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/static', methods=['GET'])
def display_graph_static():  # put application's code here


    title = 'Data Vis Project 2021'
    desc = 'A chart to viualise sentiment'

    tweets, df = get_clean_tweets('VAR')
    pos, neg, nue = part2.get_polarity(df)

    labels = ['positive', 'negative', 'neutral']
    values = [pos, neg, nue]

    pi_chart_one = zip(labels, values)

    pi_chart_two = []

    for label, value in pi_chart_one:
        pi_chart_two.append({'name': label, 'y': value})

    title1 = 'Data Vis Project 2021'
    desc1 = 'A chart to viualise sentiment'

    tweets1, df1 = get_clean_tweets('Vaccine')

    pos1, neg1, nue1 = part2.get_polarity(df1)

    labels1 = ['positive', 'negative', 'neutral']
    values1 = [pos1, neg1, nue1]

    pi_chart_three = zip(labels1, values1)

    pi_chart_four = []

    for label1, value1 in pi_chart_three:
        pi_chart_four.append({'name': label1, 'y': value1})

    title_location = 'Location bubble'
    desc_location = 'Location bubble chart'
    packed_bubble = part2.get_location(tweets)
    packed_bubble1 = part2.get_location(tweets1)
    return render_template('about.html', title=title, title1=title1, title2=title_location, description_text=desc, description_text1=desc1,
                           description_text2=desc_location, chart_name='Pie', chart_name1='Pie', chart_name2='Bubble', pi1=pi_chart_one, pi2=pi_chart_two
                           ,pb1=packed_bubble, pb2=packed_bubble1, pi3=pi_chart_three, pi4=pi_chart_four)

@app.route('/chart', methods=['POST', 'GET'])
def display_graph():  # put application's code here
    input_one = "Man United"
    if request.method == 'POST':
        input_one = request.form["query_one"]

    title = 'Data Vis Project 2021'
    desc = 'A chart to viualise sentiment'

    tweets, df = get_clean_tweets(input_one)
    pos, neg, nue = part2.get_polarity(df)

    labels = ['positive', 'negative', 'neutral']
    values = [pos, neg, nue]

    data = zip(labels, values)

    list = []

    for label, value in data:
        list.append({'name': label, 'y': value})

    title_location = 'Location bubble'
    desc_location = 'Location bubble chart'
    packed_bubble = part2.get_location(tweets)
    return render_template('chart.html', title=title, title2=title_location, description_text=desc, description_text2=desc_location,
                           chart_name='Pie', chart_name2='Bubble', data=list, data2=packed_bubble)


if __name__ == '__main__':
    app.run()
