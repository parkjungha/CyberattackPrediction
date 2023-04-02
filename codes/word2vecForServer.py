import os
import json
from collections import Counter
from gensim.models.keyedvectors import KeyedVectors
import numpy as np
from nltk.corpus import stopwords 
import preprocessor as p
import pandas as pd
from DocSim import DocSim

def getKeyword():
    filedir = '/home/itm5/slave/jh/industry_term.txt'
    str=''
    file = open(filedir,'r',encoding='utf-8')
    str = file.read()
    keywordList = str.strip().split("', '")
    keywordList = [i.lower() for i in keywordList]
    keywordList = [i.strip() for i in keywordList]
    my_set =set(keywordList)
    keywordList= list(my_set)
    return keywordList
    file.close()
    
if __name__ == '__main__':
    keywordList = getKeyword() 

    #%% Mapping Each Word with Weight 

    weightDic = {}

    for i in range(len(keywordList)):
        phrase = keywordList[i].split()
        if (len(phrase)==1):
            weightDic[keywordList[i]] = 1
        else:
            for j in range(len(phrase)):
                if (phrase[j] not in weightDic): 
                    weightDic[phrase[j]] = 1/len(phrase) 
                else: 
                    weightDic[phrase[j]] +=  1/len(phrase) 
                    if(weightDic[phrase[j]]>=1): 
                        weightDic[phrase[j]] = 1 

    del weightDic['123']
    del weightDic['17']
    del weightDic['2.9']
    del weightDic['3']
    del weightDic['300k']
    del weightDic['#macos']
    del weightDic['(default)']
    del weightDic['/mime']
    del weightDic['@nas']
    weightDic['macos'] = 0.5
    weightDic['mime'] = 0.125
    weightDic['nas'] = 1
    weightDic['default'] = 1
    
    #%% Filtering by weighting !
    # GROUP 1
    groupNum = 1
    path = '/home/itm5/slave/jh/'
    files = os.listdir(path+'gr'+str(groupNum)+'_processed')
    corpus1 = []
    for i in range(len(files)): 
        jdata = open(path+'gr'+str(groupNum)+'_processed/'+str(files[i]), encoding="utf-8").read() 
        data = json.loads(jdata) 
        print(i,str(files[i]))
        for j in data[:]:
            atweet = j['text'].split() 
            score = 0 
            for k in range(len(atweet)): 
                if (atweet[k] in weightDic): 
                    score += weightDic[atweet[k]] 
            if(score>1):
                corpus1.append([j['usernameTweet'],j['text']]) 
    
    # GROUP 2
    groupNum = 2
    files = os.listdir(path+'gr'+str(groupNum)+'_processed')
    corpus2 = []
    for i in range(len(files)): 
        jdata = open(path+'gr'+str(groupNum)+'_processed/'+str(files[i]), encoding="utf-8").read() 
        data = json.loads(jdata) 
        print(i,str(files[i]))
        for j in data[:]:
            atweet = j['text'].split() 
            score = 0 
            for k in range(len(atweet)): 
                if (atweet[k] in weightDic): 
                    score += weightDic[atweet[k]] 
            if(score>1): 
                corpus2.append([j['usernameTweet'],j['text']]) 
                
    #%% Word2vec
    model_path = '/home/itm5/slave/jh/GoogleNews-vectors-negative300.bin'
    w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
    ds = DocSim(w2v_model,stopwords=stopwords.words('english'))
    
    # GROUP 1
    groupNum = 1
    files = os.listdir(path+'gr'+str(groupNum)+'_processed')
    df1 = []

    for i in range(len(corpus1)): 
        sim_scores = ds.calculate_similarity(corpus1[i][1], keywordList) 
        df1.append([corpus1[i][0],corpus1[i][1],sum(sim_scores),sum(sim_scores)/len(sim_scores)]) 

    df1 = pd.DataFrame(df1,columns=['username','tweet text','sum','avg'])
    df1.sort_values(by='sum',ascending=False, inplace=True)
    df1.to_csv("/home/itm5/slave/jh/result_word2vec_gr1_1202.csv", sep=',', na_rep='NaN')

    # GROUP 1
    groupNum = 2
    files = os.listdir(path+'gr'+str(groupNum)+'_processed')
    df2 = []

    for i in range(len(corpus2)): 
        sim_scores = ds.calculate_similarity(corpus2[i][1], keywordList) 
        df2.append([corpus2[i][0],corpus2[i][1],sum(sim_scores),sum(sim_scores)/len(sim_scores)]) 
        
    df2 = pd.DataFrame(df2,columns=['username','tweet text','sum','avg'])
    df2.sort_values(by='sum',ascending=False, inplace=True)
    df2.to_csv("/home/itm5/slave/jh/result_word2vec_gr2_1202.csv", sep=',', na_rep='NaN')    