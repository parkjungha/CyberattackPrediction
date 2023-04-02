import pandas as pd
import string,re,json
from datetime import datetime,timedelta
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import preprocessor as p
from rake_nltk import Rake
from collections import Counter
import numpy as np

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

def textCleaning(text): #for word2vec calculation
    text = text.lower()
    text = text.translate(text.maketrans('', '', string.punctuation))
    text = re.sub('[^a-zA-Z]', ' ', text)
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text)
    result = []
    for w in word_tokens: 
        if w not in stop_words and len(w)>1: 
            result.append(w) 
    n=WordNetLemmatizer()
    lemmatized_words = [n.lemmatize(word) for word in result]
    return (' '.join(lemmatized_words))


path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/'

news2017 = pd.read_excel(path+'2017_news.xlsx', names=("id","date","title","contents"))
news2018 = pd.read_excel(path+'2018_news.xlsx', names=("id","date","title","contents"))
news2019 = pd.read_excel(path+'2019_news.xlsx', names=("id","date","title","contents"))

def setPeriod(date):
    period = []
    for i in range(-3,4):
        period.append(str(date+timedelta(days=i))[0:10])
    return period

periodList = []
for i in range(len(news2019)):
    #news2017['contents'][i] = textCleaning(news2017['contents'][i])
    periodList.append(setPeriod(news2019['date'][i]))

def makeWordList(phrases_list):
    n=WordNetLemmatizer()
    wordList=[]
    for k in phrases_list[:]:
        # if (k.isnumeric()):
        #     phrases_list.remove(k)
        #     continue
        temp = k.split()
        for j in range(len(temp)): 
            if temp[j].isalpha():
                wordList.append(n.lemmatize(temp[j]))    
    return wordList
    
    
def calculateRake(year,groupNum):
    r = Rake(min_length=1, max_length=5)
    path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/year_filtered/'
    jdata = open(path+str(year)+'/30/group'+str(groupNum)+'_processed_30.json', encoding="utf-8").read() 
    data = json.loads(jdata) 
    news2019['rake_score_gr'+str(groupNum)]=np.nan
    for j in range(len(news2019)): # 2017년의 뉴스 기사 iteration
        text = news2019['title'][j]+'. '+news2019['contents'][j]
        r.extract_keywords_from_sentences(sent_tokenize(text))
        newsWordList = makeWordList(list(r.get_ranked_phrases()))
        
        print(news2019['id'][j])
        temp = []
        for i in range(len(data)):
            if data[i]['datetime'] in periodList[j]:
                text = p.clean(data[i]['text'])
                r.extract_keywords_from_sentences([text])
                tweetWordList = makeWordList(list(r.get_ranked_phrases()))
                matching = list(set(newsWordList).intersection(tweetWordList))
                temp.append(len(matching))
        if len(temp)==0:
            news2019['rake_score_gr'+str(groupNum)][j] = 0
        else:
            news2019['rake_score_gr'+str(groupNum)][j] = sum(temp)/len(temp)
    return news2019

news2019 = calculateRake(2019,1)
news2019 = calculateRake(2019,2)
news2019 = calculateRake(2019,3)
news2019 = calculateRake(2019,4)
news2019.drop(['title', 'contents'],axis=1).to_csv("/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/news2019_rake_score.csv",encoding="utf-8")


# 여기서부턴 W2V
from gensim.models.keyedvectors import KeyedVectors

model_path = '/Users/jungh/Downloads/GoogleNews-vectors-negative300.bin'
w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
ds = DocSim(w2v_model,stopwords=stopwords.words('english'))
path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/year_filtered/'

def calculateW2v(year,groupNum):
    jdata = open(path+str(year)+'/group'+str(groupNum)+'_processed.json', encoding="utf-8").read() 
    data = json.loads(jdata) 
    news2019['w2v_score_gr'+str(groupNum)]=np.nan
    
    for j in range(len(news2019)): # 2017년의 뉴스 기사 iteration
        text = textCleaning(news2019['title'][j]+'. '+news2019['contents'][j])
        print(news2019['id'][j])
        corpus = []
        for i in range(len(data)):
            if data[i]['datetime'] in periodList[j]:
                corpus.append(data[i]['text_processed'])
        sim_scores = ds.calculate_similarity(text, corpus)
        
        if (len(sim_scores)==0):
            news2019['w2v_score_gr'+str(groupNum)][j] = 0
        else:
            news2019['w2v_score_gr'+str(groupNum)][j] = sum(sim_scores)/len(sim_scores) #word2vec score 저장

calculateW2v(2019,1)
calculateW2v(2019,2)
calculateW2v(2019,3)
calculateW2v(2019,4)
news2019.drop(['title', 'contents'],axis=1).to_csv("/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/news2019_with_score.csv",encoding="utf-8")
