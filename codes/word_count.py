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
    
def word_count(temp):
    return sorted(dict(Counter(temp.split())).items(), key = lambda x : x[1], reverse = True)[:100]
    
if __name__ == '__main__':
    keywordList = getKeyword()
    wordList=[]
    for i in range(len(keywordList)):
        wordList += keywordList[i].split()
    path= '/Users/jungh/Downloads/PredictCyberAttacks/All Tweets/all_user_processed/'
    files=os.listdir(path)
    topUser2={}
    for k in range(len(files)):
        jdata = open(path+str(files[k]),encoding="utf-8").read()
        data = json.loads(jdata)
        count = 0
        for j in range(len(data)):
            if 'exploit' in data[j]['text']:
                count += 1
        topUser2[files[k].split('.')[0]] = count
        print(k)
        
    topUser2 = sorted(topUser2.items(), key=lambda x: x[1], reverse=True) # 'exploit'이 포함된 트윗의 개수가 높은 순서대로 정렬
    
    
        
        # frequencyList = word_count(temp)
        # filteredList = [x[0] for x in frequencyList]
        # result = [x for x in filteredList if x in wordList]
        
    #0110 
    import os
    corpus = []
    path = '/Users/jungh/Downloads/PredictCyberAttacks/All Tweets/RF_user/'
    jdata = open(path+str(year)+'.json',encoding="utf-8").read()
    data = json.loads(jdata)   
    for i in range(len(data)):
        #data[i]['text'] = textCleaning(data[i]['text'])
        for j in keywordList:
            if j in data[i]['text']:
                corpus.append(data[i])
                break
            
    files = os.listdir(path)
    for i in range(len(files)):

        for k in range(len(data)):
            for j in keywordList:
                if j in data[k]['text']:
                    corpus.append(data[k])
                    break
                    
        print(i)
