import pandas as pd
from nltk.tokenize import word_tokenize
import sys
import csv


def process_file(fn='../SamantaDarko_tweets.csv'):
    data = pd.read_csv(fn, delimiter='|', header=None) # Select file to import here
    return data

if __name__ == "__main__":
    #filename = sys.argv[1]
    data = process_file()
    dic = {}
    for line in data.values:
        try:
            tweet = word_tokenize(line[3].decode('utf-8'))
        except:
            tweet = []
            print("Error tokenizing %s: encoding issues" % line[3])
        for token in tweet:
            if token in dic.keys():
                dic[token] += 1
            else:
                dic[token] = 1
    import operator
    for k, v in sorted(dic.items(), key=operator.itemgetter(1)):
        print("%s: %d" % (k, v))