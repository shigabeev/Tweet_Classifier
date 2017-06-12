import os
import sys
import numpy as np
import re
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib

def purify(str):
    # delete all URLs
    str = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', str, flags=re.MULTILINE)
    #delete all usernames
    str = re.sub(r'@\w+', '', str)
    return str.lower()

def generate_data(corpus):
    train_target = [corpus[i][1] for i in range(len(corpus))]
    train_data = [corpus[i][0] for i in range(len(corpus))]
    return train_data, train_target


if __name__ == "__main__":
    train_corpus = []
    for cat in os.listdir("classes"):
        if cat[0] != '.':
            for account in os.listdir("classes/%s" % cat):
                with open("classes/%s/%s" % (cat, account)) as fp:
                    raw_data = csv.reader(fp, delimiter = '|')
                    for line in raw_data:
                        if line[0:1] != "RT":    # ignore retweets
                            train_corpus.append([str(purify(line[3])), cat])

    train_data, train_target = generate_data(train_corpus)

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(train_data)

    tf_transformer = TfidfTransformer()
    X_train_tf = tf_transformer.fit_transform(X_train_counts)

    # here you can specify type of classifier
    if len(sys.argv) == 2:
        if sys.argv[1] == "bayes":
            from sklearn.naive_bayes import MultinomialNB
            text_clf = Pipeline([('vect', CountVectorizer()),
                                 ('tfidf', TfidfTransformer()),
                                 ('clf', MultinomialNB()), ])
        elif sys.argv[1] == "svm":
            from sklearn.linear_model import SGDClassifier
            text_clf = Pipeline([('vect', CountVectorizer()),
                                 ('tfidf', TfidfTransformer()),
                                 ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                                       alpha=1e-3, n_iter=5, random_state=42)),
                                 ])
    else:
        from sklearn.linear_model import SGDClassifier
        text_clf = Pipeline([('vect', CountVectorizer()),
                            ('tfidf', TfidfTransformer()),
                            ('clf', SGDClassifier(loss='perceptron', penalty='l2',
                                                     alpha=1e-3, n_iter=5, random_state=42)),
                            ])

    text_clf.fit(train_data, train_target)

    predicted = text_clf.predict(train_data)
    print("Точность модели тематической классификации: ", np.mean(predicted == train_target))   # show quality of model

    joblib.dump(text_clf, 'models/text_model.pkl')     # save working model

    #######
    # Gender recognition

    gender_corpus = []
    for cat in os.listdir("gender"):
        if cat[0] != '.':
            for account in os.listdir("gender/%s" % cat):
                with open("gender/%s/%s" % (cat, account)) as fp:
                    raw_data = csv.reader(fp, delimiter='|')
                    for line in raw_data:
                        if line[0:1] != "RT":  # ignore retweets
                            gender_corpus.append([purify(line[3]), cat])
    gender_data, gender_target = generate_data(gender_corpus)
    # no need for setting classifier as perceptron works perfectly well here
    gender_clf = Pipeline([('vect', CountVectorizer()),
                           ('tfidf', TfidfTransformer()),
                           ('clf', SGDClassifier(loss='perceptron', penalty='l2',
                                                 alpha=1e-3, n_iter=5, random_state=42)),
                           ])
    gender_clf.fit(gender_data, gender_target)
    predicted = gender_clf.predict(gender_data)
    print("Точность модели гендерной классификации: ", np.mean(predicted == gender_target))

    joblib.dump(gender_clf, 'models/gender_model.pkl')  # save working model
