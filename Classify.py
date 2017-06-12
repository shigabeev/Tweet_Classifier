import tweepy
import config
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
from get_tweets import get_tweets
from collections import Counter
from learn import purify
from sklearn.externals import joblib

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)
api = tweepy.API(auth)

if __name__ == "__main__":
    username = "medvedevrussia"     # default username
    if len(sys.argv) == 2:
        username = sys.argv[1]
    try:
        text_clf = joblib.load("models/text_model.pkl")
        gender_clf = joblib.load("models/gender_model.pkl")
    except FileNotFoundError:
        sys.exit("Не найден файл модели")
    get_tweets(username, folder="unsorted")
    tweets = []
    with open("unsorted/{0}_tweets.csv".format(username)) as fp:
        raw_data = csv.reader(fp, delimiter='|')
        for line in raw_data:
            if line[0:1] != "RT":  # ignore retweets
                tweets.append(purify(line[3]))

    predicted = text_clf.predict(tweets)
    result = []
    for doc, category in zip(tweets, predicted):
        result.append(category)
    z = Counter(result)
    user = api.get_user(username)
    labels = list(z)
    values = list(z.values())
    explode = [np.log(x) / 50 for x in values]

    plt.pie(values, labels=labels, explode=explode,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')

    print("\n")
    print(user.name, ", ", user.followers_count, "подписчиков.")
    print("Интересы: ")

    for value, label in zip(values, labels):
        print(label, " : %1.1f%%" % (value / len(tweets) * 100))

    gender_predict = gender_clf.predict(tweets)
    gender_result = []
    for doc, category in zip(tweets, gender_predict):
        gender_result.append(category)
    print("Пол: ", Counter(gender_result).most_common()[0][0])
    plt.show()


