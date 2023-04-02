from gensim.models.keyedvectors import KeyedVectors
import numpy as np
from nltk.corpus import stopwords 
import os,json
import preprocessor as p
import pandas as pd

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
    
keywordList = getKeyword()
    
model_path = '/Users/jungh/Downloads/GoogleNews-vectors-negative300.bin'
w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)

ds = DocSim(w2v_model,stopwords=stopwords.words('english'))

files = os.listdir('/Users/jungh/Desktop/getTweetText/gr2_processed')
df = []

for i in range(len(files)): #GroupN에 속하는 User들 모두 순회
    avg_sim_score = [] #초기화
    sentence=''
    jdata = open("/Users/jungh/Desktop/getTweetText/gr2_processed/"+str(files[i]), encoding="utf-8").read() #한 유저 파일 접근
    data = json.loads(jdata)  
    size = len(data) #특정 유저의 data size저장
    print(str(files[i]).split('.')[0]) #프린트
    if (data == []): #data가 빈 데이터면 다음사람으로 넘어가자
        continue
    for j in range(len(data)): #user데이터에서 모든 tweet text 순회
        sentence = sentence+' '+data[j]['text'] #하나의 텍스트 sentence로 저장
    sim_scores = ds.calculate_similarity(sentence, keywordList) #sentence하나와 키워드셋의 유사도 구함 (return the list consists of score for each sentence.)
    
    df.append([str(files[i]).split('.')[0],sum(sim_scores),sum(sim_scores)/len(sim_scores),size]) #유저 한명에 대해 text다 돌고 나면  avg_sim_score List의 합과 길이를 df에 추가. 나중에 csv로 저장하기 위해서

df = pd.DataFrame(df,columns=['username','sum','sum/len','size'])
df.sort_values(by='sum',ascending=False, inplace=True)
df.to_csv("/Users/jungh/Desktop/getTweetText/gr2_processed/gr2_word2vec_modified.csv", sep=',', na_rep='NaN')


jdata = open("/Users/jungh/Desktop/getTweetText/gr2_processed/"+str(files[i]), encoding="utf-8").read() #한 유저 파일 접근
data = json.loads(jdata)  
for j in range(len(data)): #user데이터에서 모든 tweet text 순회
    sentence = sentence+' '+data[j]['text']
    
    
    
from gensim.models import Word2Vec
embedding_model = Word2Vec(tokenized_contents, size=100, window = 2, min_count=50, workers=4, iter=100, sg=1)
