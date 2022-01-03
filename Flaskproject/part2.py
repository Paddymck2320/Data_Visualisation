import pandas as pd
from matplotlib import pyplot as plt


def get_polarity(tweets, neg, neu, pos):
    print(tweets[0])
    for tweet in tweets[0]:
        if tweet['sentiment'] > .25:
            pos.append(tweet)
        elif  tweet['sentiment'] < .25:
            neg.append(tweet)
        else:
            neu.append(tweet)

    return pos, neg, neu

def get_polarity1(tweets, neg, neu, pos):
    for tweet in tweets:
        if tweet.sentiment > .25:
            pos.append(tweet)
        elif  tweet.sentiment < .25:
            neg.append(tweet)
        else:
            neu.append(tweet)

    return pos, neg, neu

def display_graph(p, n, neu):
    labels = ['postitive', 'negative', 'neutral']
    values = [p, n, neu]

    plt.title('Sentiment Analysis')

    plt.pie(values, labels=labels, autopct='%1.1f%%')

    plt.show()

def display_graph1(p, n, neu):
    labels = ['postitive', 'negative', 'neutral']
    values = [p, n, neu]

    plt.title('Sentiment Analysis')

    plt.pie(values, labels=labels, autopct='%1.1f%%')

    plt.show()


if __name__ == '__main__':
    df = pd.read_csv('output.csv')
    df1 = pd.read_csv('output1.csv')

    df.set_index('id', inplace=True)
    df1.set_index('id', inplace=True)

    postitive, negative, neutral = get_polarity(df)
    postitive, negative, neutral = get_polarity1(df1)

    display_graph(postitive, negative, neutral)
    display_graph1(postitive, negative, neutral)
