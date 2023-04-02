import os
import json
from collections import Counter

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
    
keywordList = getKeyword() 

# List의 단어 하나 하나 돌면서 split하여 한개 이상의 단어 (구) 일때는 단어 개수의 inverse를 weight를 한 단어에 설정
# dictionary 형식으로 (나중에 json으로 변환할 것) 'word':'weight'으로 저장함
# 이미 그 word가 dictionar의 keys중에 있으면 value값을 비교해서 max(더 큰걸로) 교체. 
# 모든 단어에 대해서

#%% Mapping Each Word with Weight 
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
            
#%% Filtering by weighting !
groupNum = 1
path = '/Users/jungh/Downloads/PredictCyberAttacks/tweet/'
files = os.listdir(path+'gr'+str(groupNum))
corpus1 = []
for i in range(len(files)): # Group1 순회
    jdata = open(path+'gr'+str(groupNum)+'_processed/'+str(files[i]), encoding="utf-8").read() 
    data = json.loads(jdata) 
    if(size<15): # threshold = 15
        continue
    print(i,str(files[i]))
    for j in data[:]:
        if j:
            atweet = j['content'].split() # Tweet 단어 단위로 Split
            score = 0 # Score 초기화
            for k in range(len(atweet)): # 단어 하나씩 순회
                if (atweet[k] in weightDic): # keyword set에 있으면 
                    score += weightDic[atweet[k]] # 매핑되는 weight를 score에 더해줌
            if(score>1): # score가 1보다 클 때만
                corpus1.append([j['user_id'][1:],j['content']]) # 해당하는 tweet을 corpus에 추가함 

# Weight 값 맞는지 검증을 위한 Test Code            
wordList = []
for i in range(len(keywordList)):
    wordList= wordList+keywordList[i].split()

count=0 
for i in range(len(wordList)):
    if wordList[i] == 'code':
        count += 1
        