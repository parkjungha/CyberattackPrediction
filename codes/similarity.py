import pandas as pd

data = pd.read_csv('/Users/jungh/Desktop/group4_profile.csv', low_memory=False)
data['description'] = data['description'].fillna('') # description에서 Null 값을 가진 경우에는 값 제거

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['description'])
# description에 대해서 tf-idf 수행
print(tfidf_matrix.shape)

from sklearn.metrics.pairwise import linear_kernel
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
print(cosine_sim[0])