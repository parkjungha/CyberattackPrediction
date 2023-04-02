import os
import json
from collections import Counter
import preprocessor as p
import string
import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer

def getKeyword():
    filedir = '/Users/jungh/Desktop/industry_term.txt'
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

def createWeightDic():
    keywordList = getKeyword() 

    weightDic = {}
    
    for i in range(len(keywordList)):
        phrase = keywordList[i].split()
        if (len(phrase)==1):
            weightDic[keywordList[i]] = 1
        else:
            for j in range(len(phrase)):
                if (phrase[j] not in weightDic): # 이미 dictionary 안에 그 단어가 존재하지 않으면
                    weightDic[phrase[j]] = 1/len(phrase) # 1/n 값으로 저장
                else: # 이미 존재하면
                    weightDic[phrase[j]] +=  1/len(phrase) # 1/n 값 더해줌
                    if(weightDic[phrase[j]]>=1): #더했을 때 최대값인 1보다 크면
                        weightDic[phrase[j]] = 1 # 그냥 1
    # 직접 확인해서 이상한 것들 제거함..
    del weightDic['волна']
    del weightDic['лаборатория']
    del weightDic['тампере']
    del weightDic['технологического']
    del weightDic['университета']
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
    
    return weightDic

def textCleaning(text): #argument는 str
    text = p.clean(text) #URL, Mention 제거 
    text = text.lower()
    # 구두점 제거
    text = text.translate(text.maketrans('', '', string.punctuation))
    # 영문자 이외 문자는 공백으로 변환
    text = re.sub('[^a-zA-Z]', ' ', text)
    # 불용어 제거
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text)
    result = []
    for w in word_tokens: 
        if w not in stop_words and len(w)>1: 
            result.append(w) 
    # 표제어 추출 (어간추출보다 단어 복원 성능이 좋아서 선택)
    n=WordNetLemmatizer()
    lemmatized_words = [n.lemmatize(word) for word in result]
    return (lemmatized_words)

def filtering(groupNum):
    weightDic = createWeightDic()
    groupNum = 4
    path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/'
    files = os.listdir(path+'group'+str(groupNum))
    totalSize = 0
    scoreList = []
    corpus = []
    for i in range(len(files)): # GroupN 순회  
        jdata = open(path+'group'+str(groupNum)+'/'+str(files[i]), encoding="utf-8").read() 
        data = json.loads(jdata)
        totalSize += len(data)
        if(len(data)<15): # threshold = 15
            continue
        print(i,str(files[i]))
        for j in data[:]:
            atweet = textCleaning(j['text'])
            score = 0 # Score 초기화
            for k in range(len(atweet)): # 단어 하나씩 순회
                if (atweet[k] in weightDic): # keyword set에 있으면 
                    score += weightDic[atweet[k]] # 매핑되는 weight를 score에 더해줌
            scoreList.append(score)
            if(score>1): # score가 1보다 클 때만
                corpus.append(j) # 해당하는 tweet을 corpus에 추가함
                
        with open(path+'gr'+str(groupNum)+'_filtered/'+str(files[i]),'w') as makefile :
            json.dump(corpus,makefile)

# 필터링 filtering된 트윗의 비율 (개수 비교)
# totalSize와 len(corpus) 비교
print(totalSize)
print(len(corpus))
print(sum(scoreList)/len(scoreList))
    