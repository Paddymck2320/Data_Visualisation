from twitter_auth import *
from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt

def percentage(part, whole):
    return 100* float(part)/float(whole)


auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

searchTerm = input("Enter keyword/ hashtag you want to search : ")

tweets = tweepy.Cursor(api.search_tweets, q=searchTerm, lang="en").items(50)


positive = 0
negative = 0
neutral = 0
polarity = 0

for tweet in tweets:
    analysis = TextBlob(tweet.text)
    polarity += analysis.sentiment.polarity

    if (analysis.sentiment.polarity == 0):
        neutral += 1

    elif (analysis.sentiment.polarity < 0.00):
        negative += 1

    if (analysis.sentiment.polarity > 0.00):
        positive += 1

positive = percentage(positive, 50)
negative = percentage(negative, 50)
neutral = percentage(neutral, 50)

positive = format(positive, '.2f')
neutral = format(neutral, '.2f')
negative = format(negative, '.2f')


if(polarity == 0):
    print("Neutral")
elif (polarity < 0):
    print("Negative")
elif (polarity > 0):
    print("Positive")

labels = ['Positive ['+str(positive)+ '%]', 'Neutral [' + str(neutral) + '% ]', 'Negative [' + str(negative) + '%]']
sizes = [positive, neutral, negative]
colors = ['yellowgreen', 'gold', 'red']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title("How people are reacting on " + searchTerm + "by analysing Tweets.")
plt.axis('equal')
plt.tight_layout()
plt.show()