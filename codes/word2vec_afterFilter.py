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

path = '/Users/jungh/Downloads/PredictCyberAttacks/tweet/'
groupNum = 1
files = os.listdir(path+'gr'+str(groupNum)+'_processed')
df4 = []

for i in range(len(corpus4)): #GroupN에 속하는 User들 모두 순회
    sim_scores = ds.calculate_similarity(corpus4[i][1], keywordList) # tweet 하나와 키워드셋의 유사도 구함 (return the list consists of score for each sentence.)
    if (len(sim_scores)==0):
        continue
    df4.append([corpus4[i][0],corpus4[i][1],sum(sim_scores),sum(sim_scores)/len(sim_scores)]) # 유저 이름, 트윗 텍스트, sum of similarity, mean of similarity *어차피 분모 똑같이 517?이라서 의미 없을듯
    print(i)

df4 = pd.DataFrame(df4,columns=['username','tweet text','sum','avg'])
df4.sort_values(by='sum',ascending=False, inplace=True)
df4.to_csv("/Users/jungh/Downloads/PredictCyberAttacks/tweet/word2vec_gr4_1222.csv", sep=',', na_rep='NaN')

count = df4.groupby('username').count()
mean = df4.groupby('username').mean()
count.drop(['tweet text','sum'],axis = 1,inplace=True)
mean.drop(['sum'],axis = 1,inplace=True)

merge = pd.merge(mean,count,on="username")
merge.columns=['score','size']
merge.sort_values(by='score',ascending=False, inplace=True)
merge.to_csv("/Users/jungh/Downloads/PredictCyberAttacks/tweet/grby4_w2v_1222.csv", sep=',', na_rep='NaN')

# groupbyUser = df2.groupby('username').average()

groupbyUser.to_csv("/Users/jungh/Desktop/getTweetText/grby2_word2vec.csv", sep=',', na_rep='NaN')

gr1result = pd.read_csv('/Users/jungh/Desktop/getTweetText/word2vec_gr1_1202.csv')
gr1result.drop(['Unnamed: 0'],inplace=True,axis=1)

gr2result = pd.read_csv('/Users/jungh/Desktop/getTweetText/word2vec_gr2_1202.csv')
gr2result.drop(['Unnamed: 0'],inplace=True,axis=1)


mean1 = gr1result.groupby('username').mean()
mean2 = gr2result.groupby('username').mean()
sum1 = gr1result.groupby('username').sum()
sum2 = gr2result.groupby('username').sum()
mean1.sort_values(by='avg',ascending=False, inplace=True)
mean2.sort_values(by='avg',ascending=False, inplace=True)

mean1.to_csv("/Users/jungh/Desktop/getTweetText/grby1_word2vec_1206.csv", sep=',', na_rep='NaN')
mean2.to_csv("/Users/jungh/Desktop/getTweetText/grby2_word2vec_1206.csv", sep=',', na_rep='NaN')
