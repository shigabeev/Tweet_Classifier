import json
import csv
import numpy as np
import re
import sys
import copy
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from get_tweets import get_tweets

# this script should have been returning chance of test_data's tweet belonging to classes of learn_data

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
    for username in ["meduzaproject", "Stalingulag", "brupsen", "rianru", "hclokomotiv"]:
        if len(sys.argv) == 2:
            username = sys.argv[1]
        get_tweets(username, 10)
        DB = "DB.json"
        folder = "unsorted"
        try:
            dic = json.load(open(DB, 'r'))
        except:
            print("error reading file. Terminating")
            dic = {}
            quit()
        cats = [line.rstrip('\n') for line in open('labels.txt')]   # list of categories
        for clf in [MultinomialNB(), svm.SVC(), KNeighborsClassifier()]:
            print(clf)
            X = np.transpose(list(dic.values()))
            y = cats
            clf.fit(X, y)
            test_data = get_words("unsorted/%s_tweets.csv" % username)
            dic_test = copy.deepcopy(dic)
            count = [0] * len(cats)
            for tweet in test_data:
                for i in dic_test:  # clear dictionary
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



