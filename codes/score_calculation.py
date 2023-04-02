import os,json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as datetime
import preprocessor as p
import string
import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer
from gensim.models.keyedvectors import KeyedVectors
from rake_nltk import Rake
from collections import Counter


class DocSim:
    def __init__(self, w2v_model, stopwords=None):
        self.w2v_model = w2v_model
        self.stopwords = stopwords if stopwords is not None else []

    def vectorize(self, doc: str) -> np.ndarray:
        """
        Identify the vector values for each word in the given document
        :param doc:
        :return:
        """
        doc = doc.lower()
        words = [w for w in doc.split(" ") if w not in self.stopwords]
        word_vecs = []
        for word in words:
            try:
                vec = self.w2v_model[word]
                word_vecs.append(vec)
            except KeyError:
                # Ignore, if the word doesn't exist in the vocabulary
                pass

        # Assuming that document vector is the mean of all the word vectors
        # PS: There are other & better ways to do it.
        vector = np.mean(word_vecs, axis=0)
        return vector

    def _cosine_sim(self, vecA, vecB):
        """Find the cosine similarity distance between two vectors."""
        csim = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
        if np.isnan(np.sum(csim)):
            return 0
        return csim

    def calculate_similarity(self, source_doc, target_docs=None, threshold=0):
        """Calculates & returns similarity scores between given source document & all
        the target documents."""
        if not target_docs:
            return []

        if isinstance(target_docs, str):
            target_docs = [target_docs]

        source_vec = self.vectorize(source_doc)
        results = []
        for doc in target_docs:
            target_vec = self.vectorize(doc)
            sim_score = self._cosine_sim(source_vec, target_vec)
            if sim_score > threshold:
                #results.append({"score": sim_score, "doc": doc})
                results.append(sim_score)
            # Sort results by score in desc order
            #results.sort(key=lambda k: k["score"], reverse=True)
            results.sort(reverse=True)

        return results
    
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
    
def textCleaning(text): #argument는 str
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
    return (' '.join(lemmatized_words))

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

def calculate_score(year):
    
    path = '/Users/jungh/Downloads/PredictCyberAttacks/All Tweets/226/'
    jdata = open(path+str(year)+'.json', encoding="utf-8").read() 
    data = json.loads(jdata) 
    
    for i in range(len(data)):
        text = p.clean(data[i]['text']) #URL, Mention 제거 

        r.extract_keywords_from_sentences([text])
        phrases_list = list(r.get_ranked_phrases())
        
        wordList=[] # phrase를 word단위로 잘라서 담기 위한 list 선언
        for k in phrases_list[:]:
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
        data[i]['rake_score'] = score
    
        text = textCleaning(text) # 텍스트 전처리 for word2vec calculation
        sim_scores = ds.calculate_similarity(text, keywordList) # tweet 하나와 키워드셋의 유사도 구함
        if (len(sim_scores)==0):
            data[i]['w2v_score'] = 0
        else:
            data[i]['w2v_score'] = sum(sim_scores)/len(sim_scores) #word2vec score 저장

        data[i]['text_processed'] = text # 전처리 된 텍스트 따로 저장
        data[i]['datetime'] = data[i]['datetime'][0:10]
        print(str(i)+" Processing...")
        
    df = pd.DataFrame(data)
    df_mean = df.groupby('datetime').mean()
    rake = df_mean['rake_score'].to_json()
    w2v = df_mean['w2v_score'].to_json()
    
    with open(path+str(year)+'_processed'+'.json','w') as makefile :
        json.dump(data,makefile)
    with open(path+str(year)+'_rake.json','w') as makefile :
        json.dump(rake,makefile)
    with open(path+str(year)+'_w2v.json','w') as makefile :
        json.dump(w2v,makefile)
   
if __name__ == '__main__':
    keywordList = getKeyword()
                
    r = Rake(min_length=1, max_length=5)
    n=WordNetLemmatizer()
    
    model_path = '/Users/jungh/Downloads/GoogleNews-vectors-negative300.bin'
    w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
    ds = DocSim(w2v_model,stopwords=stopwords.words('english'))
    
    weightDic = createWeightDic()
    
    calculate_score(2018)
    calculate_score(2017,2)
    calculate_score(2017,3)
    calculate_score(2017,4)
    
    calculate_score(2018,1)
    calculate_score(2018,2)
    calculate_score(2018,3)
    calculate_score(2018,4)

    calculate_score(2019,1)
    calculate_score(2019,2)
    calculate_score(2019,3)
    calculate_score(2019,4)

calculate_score(2017)
calculate_score(2018)
calculate_score(2019)