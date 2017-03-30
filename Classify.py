import json
import csv
import numpy as np
import re
import sys
import tweepy
from sklearn.naive_bayes import MultinomialNB

# this script should have been returning chance of test_data's tweet belonging to classes of learn_data


def get_tweets(username, number_of_tweets=200):
    consumer_key = "jrZm2GZjGnU4JxbmpKZje07rI"
    consumer_secret = "iFo9KzSqr7bbYz8WTUNXjGKSBKn4pQD493ZClKFGWBB35QLZqK"
    access_key = "700836102379216896-bX4bTbWPTJKtwgUXU8KyqLuBNAqqggY"
    access_secret = "alkeegvlqn7TTOtxPcM6GLAPppSPaYqhQNNLMFARi8h4q"

    # http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # set count to however many tweets you want; twitter only allows 200 at once
    # number_of_tweets = 20

    # get tweets
    tweets = api.user_timeline(screen_name=username, count=number_of_tweets)

    # create array of tweet information: username, tweet id, date/time, text
    tweets_for_csv = [[username, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in tweets]

    # write to a new csv file from the array of tweets
    print("writing to test_data/{0}_tweets.csv".format(username))
    with open("test_data/{0}_tweets.csv".format(username), 'w+') as fh:
        writer = csv.writer(fh, delimiter='|')
        writer.writerows(tweets_for_csv)


def get_words(csv_file, row=3, delimiter = '|'):
    with open(csv_file) as fp:
        data = csv.reader(fp, delimiter = delimiter)
        tweets = []
        for line in data:
            words = line[row].lower()
            if words[0:1] == "RT":  # ignore retweets
                continue
            # next line for deleting all URLs in tweet
            words = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', words, flags=re.MULTILINE)
            words = re.findall(r'\w+', words)
            tweets.append(words)
        return tweets

if __name__ == "__main__":
    # default
    username = "meduzaproject"
    if len(sys.argv) == 2:
        username = sys.argv[1]
        get_tweets(username)
    DB = "DB.json"
    folder = "test_data"
    try:
        dic = json.load(open(DB, 'r'))
    except:
        print("error reading file. Terminating")
        dic = {}
        quit()
    cats = [line.rstrip('\n') for line in open('labels.txt')]   # list of categories
    clf = MultinomialNB()
    X = np.transpose(list(dic.values()))
    y = cats
    clf.fit(X, y)
    mode = "partial"    # 2 modes: partial and whole. "partial" returns number of tweets for each category.

    if mode == "partial":
        test_data = get_words("test_data/%s_tweets.csv" % username)
        dic_test = dic
        count = [0] * len(cats)
        for tweet in test_data:
            for i in dic_test:
                dic_test[i] = 0
            for word in tweet:
                if word in dic_test:
                    dic_test[word] += 1
                else:
                    continue
            cat = clf.predict(np.array(list(dic_test.values())).reshape(1, -1))
            for i, _ in enumerate(cats):
                if cat == cats[i]:
                    count[i] += 1
                    break
                # if (clf.predict(np.array(list(dic_test.values())).reshape(1, -1))) == cats[i]:
                #     count[i] += 1
        for i, cat in enumerate(cats):
            print("Number of %s tweets: %s" % (cats[i], count[i]))
    else:   # "whole" mode. Returns category for whole account (first 200 tweets)
        test_data = get_words("test_data/%s_tweets.csv" % username)
        dic_test = dic
        for i in dic_test:  # clean new dic
            dic_test[i] = 0
        count = [0] * len(cats)
        for tweet in test_data:
            for word in tweet:
                if word in dic_test:
                    dic_test[word] += 1
                else:
                    continue
        cat = clf.predict(np.array(list(dic_test.values())).reshape(1, -1))
        print("Dominant category is %s" % cat)
    # OK, this is raw AF


