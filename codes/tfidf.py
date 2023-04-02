import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import os

def read_txt(filename,sep=''):
    str=''
    file = open(filename,'r',encoding='utf-8')
    str = file.read()
    li = str.strip().split(sep)
    return li
    file.close()

def tfidfUsingKeywordSet(keywordList):
    return TfidfVectorizer(vocabulary=keywordList, ngram_range = (1, 2))

def tfidfUsingTextOnly():
    return TfidfVectorizer(max_features=100, ngram_range = (1, 2)) 

def display_scores(tfidf, tfs):
    scores = zip(tfidf.get_feature_names(), np.asarray(tfs.sum(axis=0)).ravel())
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    for item in sorted_scores[:100]:
        print ("{0:50} Score: {1}".format(item[0], item[1]))

def calculateSum(tfidf, tfs):
    sum=0
    feature_len = len(tfidf.get_feature_names())
    scores = zip(tfidf.get_feature_names(), np.asarray(tfs.sum(axis=0)).ravel())
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    for item in sorted_scores:
        sum += item[1]
    print(feature_len)
    return(sum)

if __name__ == '__main__':
    keywordList = read_txt('/Users/jungh/Desktop/industry_term.txt',sep="', '")
    keywordList = [i.lower() for i in keywordList]
    my_set =set(keywordList)
    keywordList= list(my_set)

    files = os.listdir('/Users/jungh/Desktop/getTweetText/gr1_processed')
    df = []
    for i in range(len(files)):
        jdata = open("/Users/jungh/Desktop/getTweetText/gr1_processed/"+str(files[i]), encoding="utf-8").read()
        data = json.loads(jdata)
        size = len(data)
        if (data == []):
            continue
        corpus = []
        for j in range(len(data)):
            corpus.append(data[j]['text'])

        tfidf1 = tfidfUsingKeywordSet(keywordList)
        tfidf1_result = tfidf1.fit_transform(corpus)
        df.append([str(files[i]).split('.')[0],calculateSum(tfidf1,tfidf1_result), size])

    df = pd.DataFrame(df,columns=['username','score','size'])
    df.sort_values(by='score',ascending=False, inplace=True)
    print(df.head())
    print(df.describe)
    #df.to_csv("/Users/jungh/Desktop/getTweetText/gr2_processed/TFIDF_gr1.csv", sep=',', na_rep='NaN')

#FOR THE TEST
    jdata = open("/Users/jungh/Desktop/getTweetText/gr1_processed/admdeJong.json", encoding="utf-8").read()
    data = json.loads(jdata)
    corpus= []
    for j in range(len(data)):
        corpus.append(data[j]['text'])
    tfidf1 = tfidfUsingKeywordSet(keywordList)
    tfidf1_result = tfidf1.fit_transform(corpus)
    calculateSum(tfidf1,tfidf1_result)
    display_scores(tfidf1,tfidf1_result)
