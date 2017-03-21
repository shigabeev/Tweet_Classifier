import os
import re
import csv
import json

# This script takes all files from folder train_data and save its content into dictionary DB.json in simplified form.
# All the data is tokenized and somehow vectorized to following:
# dic = {
#     "hello":[1, 0],
#     "world":[0, 1]
# }
# dic[hello][0] stands for number of occurences in first document and dic[hello][1] stands for second document

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
    folder = "train_data"
    dic = {}
    files = os.listdir(folder)
    for i, file in enumerate(files):    # prepare files list
        if file[0] == '.':    # Skip hidden files
            files.remove(files[i])
            continue
        if os.path.splitext(file)[1] != '.csv':   # Skip unsupported files
            files.remove(files[i])
            continue
    print(files)
    for i, fn in enumerate(files):
        for tweets in get_words("%s/%s" % (folder, fn)):
            for word in tweets:
                if word in dic:
                    dic[word][i] += 1
                else:
                    dic[word] = [0]*len(files)
                    dic[word][i] = 1
    with open("DB.json", 'w') as f:
        json.dump(dic, f, ensure_ascii=False)
