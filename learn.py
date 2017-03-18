import os
import re
import csv
import json

if __name__ == "__main__":
    folder = "Data"
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
        with open("%s/%s" % (folder, fn), 'r', encoding="utf-8") as csvfile:
            data = csv.reader(csvfile, delimiter = '|')
            for line in data:
                words = line[3].lower()
                if words[0:1] == "RT":  # ignore retweets
                    continue
                # next line for deleting all URLs in tweet
                words = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', words, flags=re.MULTILINE)
                words = re.findall(r'\w+', words)
                for word in words:
                    if word in dic:
                        dic[word][i] += 1
                    else:
                        dic[word] = [0]*len(files)
                        dic[word][i] = 1
    with open("DB.json", 'w') as f:
        json.dump(dic, f, ensure_ascii=False)
    print(dic)
