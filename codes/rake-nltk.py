from rake_nltk import Rake
import os
import json
import string,re
import preprocessor as p
import nltk
import pandas as pd
import preprocessor as p
from nltk.stem import PorterStemmer,WordNetLemmatizer
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
    
if __name__ == '__main__':
    keywordList = getKeyword() #Get industry keywordset provided from Recorded_future
    
    groupNum = 4
    path = '/Users/jungh/Downloads/PredictCyberAttacks/tweet/'
    files = os.listdir(path+'gr'+str(groupNum))
    rake_corpus4 = []
    
    n=WordNetLemmatizer()
    #ps = PorterStemmer() #To stem words
    r = Rake(min_length=1, max_length=5)

    for i in range(len(files)):  
        jdata = open(path+'gr'+str(groupNum)+'/'+str(files[i]), encoding="utf-8").read() 
        #Rake-nltk 알고리즘이 stopwords, punctuation characters를 통해서 phrase를 나누기 때문에 preprocessing 하기 전 트윗 텍스트 데이터를 사용
        data = json.loads(jdata) 
        size = len(data)        
        if(size<15): # threshold = 15
            continue
        print(str(i)+" "+str(files[i])) #진행상황을 보기위한 용도
        
        for j in range(len(data)):
            if data[j]:
                text = p.clean(data[j]['content']) # URL,mention 제거
                text = text.strip() # 앞뒤 공백 제거
                text = ' '.join(text.split()) # 글자 사이에 다중공백 -> 하나의 공백
                atext = re.sub('[^a-zA-Z\s+]', '', text) # 영어 이외에 문자 제거
                if ((atext=='') or (len(atext)<10)): # 10자 이내의 너무 짧은 트윗들 제거
                    continue
                atweet = atext.split()
                atweet = [n.lemmatize(word) for word in atweet] # lemmatizer 사용
    
                #atweet = [ps.stem(i) for i in atweet] # Porter Stemmer를 사용해서 원형으로 변환 (ex ing제거, s제거)
                
                score = 0 # Score 초기화
                for k in range(len(atweet)): # 단어 하나씩 순회
                    if (atweet[k] in weightDic): # keyword set에 있으면 
                        score += weightDic[atweet[k]] # 매핑되는 weight를 score에 더해줌
                if(score>1): # score가 1보다 클 때만
                    rake_corpus4.append([data[j]['user_id'][1:],text]) # corpus list에 추가
           
    # 개별 트윗에서 Keyword 추출하여 WordList 만들기
    df4 = []
    for i in rake_corpus4[:]: #corpus list 순회
        r.extract_keywords_from_sentences([i[1]]) # rake-nltk에서 제공하는 method로 문장(=트윗 하나)에서 keyword를 추출한다.  
        phrases_list = list(r.get_ranked_phrases()) # 추출된 keyword를 phrase list에 담는다
        wordList=[] # phrase를 word단위로 잘라서 담기 위한 list 선언
        for k in phrases_list[:]:
            #if (k[0]==1.0): # rank가 1인 phrase는 제거하기 위한 코드 **일단 빼지말자.. 나중에 함 더 생각
            #    phrases_list.remove(k)
            #    continue
            if (k.isnumeric()): # phrase가 숫자로만 된 경우는 지움
                phrases_list.remove(k)
                continue
            
            temp = k.split() # 공백 기준, word로 분할
            for j in range(len(temp)): 
                wordList.append(n.lemmatize(temp[j])) #분할하여 word list에 담고
        
        counter = dict(Counter(wordList)) #개수 세기
        
        score = 0 
        for key, value in counter.items():
            if (key in weightDic):
                score += value*weightDic[key] # 한 트윗에서 추출된 단어 count해서 빈도수 * 해당 단어의 Weight
        df4.append([i[0],i[1],score])

        #wordList = list(set(wordList)) #중복 제거
        
        # keywordset과 비교해서 겹치는 단어들 추출. matching이라는 list에 담음
        #matching=list(set(keywordList).intersection(wordList))    
        #if len(matching) == 0:
        #    corpus.remove(i)
        
        # Dataframe에 username, text 내용, matching word 개수, matching된 단어들. 순서로 저장 / 개별 tweet별로
        #df.append([i[0],i[1],len(matching),','.join(matching)])

        
    #비교해서 공통되는 단어 갯수 
    df4 = pd.DataFrame(df4,columns=['username','tweet text','score'])
    df4.sort_values(by='score',ascending=False, inplace=True) # 정렬
    df4.to_csv("/Users/jungh/Downloads/PredictCyberAttacks/tweet/rake_gr4_1222.csv", sep=',', na_rep='NaN')
    
    # 트윗별로 말고 user별로 보기 위해 groupby
    groupby = df2.groupby('username').count()
    groupby.to_csv("/Users/jungh/Desktop/getTweetText/groupby1.csv", sep=',', na_rep='NaN')

    df1 = pd.read_csv('/Users/jungh/Desktop/getTweetText/rake_gr2_mod.csv')
    
    # matching 개수가 없는 것들은 다 빼고 저장. 
    not_zero = df['matching'] != 0
    df_not0 = df[not_zero]
    groupby_notzero = df_not0.groupby('username').count()
    groupby_notzero.to_csv("/Users/jungh/Desktop/getTweetText/grby2_notzero.csv", sep=',', na_rep='NaN')
    
    #단어 개수 세기 Counter
    words = []
    
    for i in range(len(df)):
        words = words + df['words'][i].split(',')

    di = dict(Counter(words))
    
    import operator
    sorted_d = dict(sorted(di.items(), key=operator.itemgetter(1),reverse=True))

    with open('/Users/jungh/Desktop/getTweetText/rake_topwords_gr2.json','w') as f:
        json.dump(sorted_d,f)
        
    
    #12/06 추가
    gr1result = pd.read_csv('/Users/jungh/Desktop/getTweetText/rake_gr1_1202.csv')
    gr2result = pd.read_csv('/Users/jungh/Desktop/getTweetText/rake_gr2_1202.csv',encoding='cp949')
    mean3 = df3.groupby('username').mean()
    mean2 = gr2result.groupby('username').mean()

    mean1.sort_values(by='score',ascending=False, inplace=True)
    mean2.sort_values(by='score',ascending=False, inplace=True)
    
    mean1.to_csv("/Users/jungh/Desktop/getTweetText/grby1_rake_1206.csv", sep=',', na_rep='NaN')
    mean2.to_csv("/Users/jungh/Desktop/getTweetText/grby2_rake_1206.csv", sep=',', na_rep='NaN')

    #1222
    groupby = df4.groupby('username').count()
    groupby.drop(['tweet text'],axis = 1,inplace=True)
    mean = df4.groupby('username').mean()
    merge = pd.merge(mean,groupby,on="username")
    merge.columns=['score','size']
    merge.sort_values(by='score',ascending=False, inplace=True)
    merge.to_csv("/Users/jungh/Downloads/PredictCyberAttacks/tweet/grby4_rake_1222.csv", sep=',', na_rep='NaN')
