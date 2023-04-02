import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import nltk 
import string
import re

data_df = pd.read_json("/Users/jungh/Desktop/getTweetText/group1_modified/_jsoo_.json", lines=True)
print(data_df[0])

def load_data():
    json_data = open('/Users/jungh/Desktop/group4.json').read()
    data = json.loads(json_data)
    return data

def remove_punct(text):
    text  = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    return text
#df['Tweet_punct'] = df['Tweet'].apply(lambda x: remove_punct(x))
#df.head(10)


def remove_stopwords(text):
    stopword = nltk.corpus.stopwords.words('english')
    text = [word for word in text if word not in stopword]
    return text
#df['Tweet_nonstop'] = df['Tweet_tokenized'].apply(lambda x: remove_stopwords(x))
#df.head(10)

#Stemming
ps = nltk.PorterStemmer()
def stemming(text):
    text = [ps.stem(word) for word in text]
    return text
#df['Tweet_stemmed'] = df['Tweet_nonstop'].apply(lambda x: stemming(x))
#df.head()






