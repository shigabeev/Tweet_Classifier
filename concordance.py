import json
import sys
import os
import re

if __name__ == "__main__":
    # Settings
    left = 2
    right = 2
    start_line = 30
    end_line = 1000         # None for unlimited
    read = None           # JSON file to read, argv[4]
    export = "DB.json"
    folder = "Data"
    # defaults override
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    if len(sys.argv) > 2:
        left = int(sys.argv[2])
    if len(sys.argv) > 3:
        right = int(sys.argv[3])
    if len(sys.argv) > 4:
        read = sys.argv[4]
    # /settings
    dic = {}
    if read:
        with open(read, 'r') as fp:
            try:
                dic = json.load(fp)
            except:
                dic = {}
    for filename in os.listdir(folder):
        if filename[0] == '.':
            continue
        with open("%s/%s" % (folder, filename), 'r', encoding="utf-8") as f:
            for line in f.readlines()[start_line:end_line]:
                words = re.findall(r'\w+', line.lower())        # Tokenizing
                for i, word in enumerate(words):
                    if word not in dic:
                        dic[word] = []
                    for l in range(1, left+1):
                        if i > l-1:
                            if words[i-l] not in dic[word]:
                                dic[word].append(words[i - l])
                    for r in range(1, right+1):
                        if i < len(words) - r:
                            if words[i + r] not in dic[word]:
                                dic[word].append(words[i + r])
    with open(export, 'w') as f:
        json.dump(dic, f, ensure_ascii=False)

# TODO
# Сделать так чтобы принимал параметры. Больше контекста жрать и учитывать положение в предложении. - Done
# Принимает 4 параметра: папка с вводными файлами (может быть несколько) - Done
# Левый и правый контекст — сколько слов влево, сколько слов вправо - Done
# Учитывать ли границу предложения
# Принудительное ограничение количества слов.
# Улучшить работу с памятю. Использовать кольцевой буфер
#
