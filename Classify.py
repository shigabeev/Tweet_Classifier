import json
import csv
import numpy as np
import re

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
    DB = "DB.json"
    folder = "test_data"
    try:
        dic = json.load(open(DB, 'r'))
    except:
        print("error reading file. Terminating")
        dic = {}
        quit()
    sum = np.array([0, 0])
    for tup in dic.values():
        sum += tup
    words = get_words("test_data/meduzaproject_tweets.csv")
    # OK, this is raw AF
