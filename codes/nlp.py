import json
import string
import re
import os
import pandas as pd
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import preprocessor as p

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
    #stemmer = PorterStemmer()
    #stemmer_words = [stemmer.stem(word) for word in result]
    return (' '.join(lemmatized_words))

def tfidfMatrix(corpus,username):
    tfidfv = TfidfVectorizer().fit(corpus)
    tfidf_dict = tfidfv.get_feature_names()
    data_array = tfidfv.transform(corpus).toarray()
    data = pd.DataFrame(data_array, columns=tfidf_dict)
    data.to_csv('/Users/jungh/Desktop/getTweetText/group2_text_processed/'+username+'_tfidf.csv', sep=',', na_rep='NaN') #결과로 나온 Dataframe을 CSV로 저장
    return data
    
if __name__ == '__main__':
    files = os.listdir('/Users/jungh/Downloads/PredictCyberAttacks/tweet/gr4')
    for i in range(len(files)):
        #corpus = []
        print(str(files[i])+" Processing...")
        jdata = open("/Users/jungh/Downloads/PredictCyberAttacks/tweet/gr4/"+str(files[i]),encoding="utf-8").read() #해당 user에 대한 모든 text가 들어있는 json file
        data = json.loads(jdata)
        for j in range(len(data)):
            if data[j]:
                data[j]['content'] = textCleaning(data[j]['content']) #text 하나하나에 대해서 cleaning 하고, corpus에 추가
            #corpus.append(data[j]['text']) #group1에 속하는 모든 text를 group1의 corpus에 추가
        with open("/Users/jungh/Downloads/PredictCyberAttacks/tweet/gr4_processed/"+str(files[i]), 'w', encoding='utf-8') as make_file:
            json.dump(data,make_file) #변환된 text를 저장 user한명당 하나의 파일로 저장함
        print("Done!")
        #tfidfMatrix(corpus,str(files[i]).split('.')[0]) #group1의 corpus에 대해서 tfidf matrix생성