import numpy as np
import math
import csv
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


# Bag of Words
def getVocabulary(df):
    """
    Given a DataFrame (a corpus of documents), we want to extract all the vocabulary that is
    present in all the documents
    """
    vocab = set()
    for _, doc in df.iterrows():
        for word in doc['rapport'].split():
            vocab.add(word)
    return vocab

def getBBow(df, vocabulary):
    """
    Given a DataFrame and a dictionnary of vocabulary, we will count the amount of
    times certain words appear in each sentence
    """
    mydict = {idx: vocabulary.copy() for idx, _ in df.iterrows()}
    for idx, rows in df.iterrows():
        for word in rows['rapport'].split():
            mydict[idx][word] += 1
    return mydict

def getLBow(df, ngrams = 1):
    """
    Using the python library sklearn, we will obtain the bag of words
    """
    vectorizer = CountVectorizer(ngram_range=(ngrams, ngrams))
    X = vectorizer.fit_transform(df['rapport'].values.tolist())
    return X.toarray(), vectorizer.get_feature_names_out()

# TF-IDF
def getTF(df, vocabulary):
    mydict = {idx: vocabulary.copy() for idx, _ in df.iterrows()}
    for idx, row in df.iterrows():
        N = len(row['rapport'].split())
        for word in row['rapport'].split():
            mydict[idx][word] +=1
        for word, freq in mydict[idx].items():
            mydict[idx][word] = freq/N
    return mydict

def getIDF(df, vocabulary):
    N = df.shape[0]
    mydict = vocabulary.copy()
    for word in list(mydict.keys()):
        for _, row in df.iterrows():
            if word in row['rapport'].split():
                mydict[word]+=1
    for k, v in mydict.items():
        mydict[k] = 1 + np.log(N/v)
    return mydict

def getTfIdfManual(df, dict1, dict2):
    mydict = {idx: dict1[idx].copy() for idx, _ in df.iterrows()}
    for k, v in mydict.items():
        for word, freq in v.items():
            mydict[k][word] *= dict2[word]
    return mydict

def TF_IDF(df):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['rapport'].values.tolist())
    return X.toarray(), vectorizer.get_feature_names_out()