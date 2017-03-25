import os
import re
import csv
import json
import numpy as np
from sklearn.naive_bayes import MultinomialNB
import tweepy

# This script takes all files from folder train_data and save its content into dictionary DB.json in simplified form.
# All the data is tokenized and somehow vectorized to following:
# dic = {
#     "hello":[1, 0],
#     "world":[0, 1]
# }
# dic[hello][0] stands for number of occurences in first document and dic[hello][1] stands for second document


def get_tweets(username, number_of_tweets=20):
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
        return tweets   # returns tokenized array of words. ex: ["hello", "world"]

if __name__ == "__main__":
    # Learning
    folder = "classes"
    dic = {}  # categories or classes. Class is restricted word
    cats = os.listdir(folder)
    for i, category in enumerate(cats):
        if category[0] == '.':
            cats.remove(category)
            continue
        for fn in os.listdir("%s/%s" % (folder, category)):  # Learning process
            fp = "%s/%s/%s" % (folder, category, fn)
            if fn[0] == '.':    # Skip hidden files
                continue
            if os.path.splitext(fn)[1] != '.csv':   # Skip unsupported files
                continue
            else:
                for tweets in get_words(fp):
                    for word in tweets:
                        if word in dic:
                            dic[word][i] += 1
                        else:
                            dic[word] = [0]*len(cats)
                            dic[word][i] = 1
    with open("DB.json", 'w') as f:
        json.dump(dic, f, ensure_ascii=False)
    with open("labels.txt", 'w') as f:
        for cat in cats:
            f.write("%s\n" % cat)




