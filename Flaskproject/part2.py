import pandas as pd
from matplotlib import pyplot as plt


def get_polarity(tweets):
    return (tweets['sentiment'] > .25).sum(), (tweets['sentiment'] < -.25).sum(), (
        tweets['sentiment'].between(-.25, .25)).sum()

def get_location(tweets):
    dictionary_of_locations=[]
    locations=[]


    for tweet in tweets.current_page:
        if tweet.user.location not in locations:
            locations.append(tweet.user.location)

    for name in locations:
        if name!="" and name!=" ":
            dictionary_of_locations.append({"name":name, "value":0})

    for tweet in tweets.current_page:
        for location in dictionary_of_locations:
            if tweet.user.location == location['name']:
                location['value'] += 1

    return dictionary_of_locations

def display_graph(p, n, neu):
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
    postitive1, negative1, neutral1 = get_polarity(df1)

    display_graph(postitive, negative, neutral)
    display_graph(postitive1, negative1, neutral1)
