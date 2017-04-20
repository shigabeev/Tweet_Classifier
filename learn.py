import os
import re
import csv
import json
import tweepy
import config

# This script takes all files from folder train_data and save its content into dictionary DB.json in simplified form.
# All the data is tokenized and somehow vectorized to following:
# dic = {
#     "hello":[1, 0],
#     "world":[0, 1]
# }
# dic[hello][0] stands for number of occurrences in first document and dic[hello][1] stands for second document
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
    dic = {}
    cats = os.listdir(folder)   # categories or classes. Class is restricted word
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




