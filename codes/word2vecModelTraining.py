from gensim.models import Word2Vec

with open('C:/Users/jungh/Desktop/getTweetText/corpus/merged_corpus.txt', 'r') as f:
    list_file = []
    for line in f:
        list_file.append(line)

for i in range(len(list_file)):
    list_file.remove('\n')

for i in range(len(list_file)):
    list_file[i] = list_file[i][:-2].split()
    
with open('/Users/jungh/Desktop/getTweetText/corpus/corpus.txt', 'w') as f:
    for item in list_file:
        f.write("%s\n" % item)
    
with open('C:/Users/jungh/Desktop/getTweetText/corpus/corpus.txt', 'r') as f:
    list_file = []
    for line in f:
        list_file.append(line)
        
#with open("/Users/jungh/Desktop/getTweetText/corpus/corpus.txt", "w") as file:
#    file.writelines(list_file)
        
model = Word2Vec(list_file,size=100, window=5, min_count=5, workers=4)

model.save("word2vec.model")

model = Word2Vec.load("C:/Users/jungh/Downloads/PredictCyberAttacks/word2vec.model")
model.train([["hello", "world"]], total_examples=1, epochs=1)

vector = model.wv['computer'] 

word_vectors=model.wv
vocabs = word_vectors.vocab.keys()
word_vectors_list = [word_vectors[v] for v in vocabs]

print(word_vectors.similarity(w1='security',w2='threat'))


words = list(model.wv.vocab)

w1 = ['exploit']
model.wv.most_similar(positive=w1,topn=10)

from sklearn.decomposition import PCA
from matplotlib import pyplot

X = model[model.wv.vocab]
pca = PCA(n_components=2)
result = pca.fit_transform(X)
# create a scatter plot of the projection
pyplot.scatter(result[:, 0], result[:, 1])
words = list(model.wv.vocab)
for i, word in enumerate(words):
	pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
pyplot.show()comiche', 'noioso', 'lottusit', 'dellasap', 'macch', 'gergo', 'matteuccio', 'appunt', 'unaltr', 'telecamera', 'qst', 'ipotes', 'poveracci', 'esisteva', 'liberticida', 'cugini', 'puca', 'agitando', 'terminu', 'difficoult', 'domandarsi', 'ripetono', 'carrozzone', 'stipendio', 'apartitica', 'iniuri', 'narcisistic', 'virata', 'mestiere', 'dissidentsjournalists', 'azionista', 'votazioni', 'plagio', 'imbattibil', 'infettat', 'ritirato', 'lungi', 'ahahhahah', 'ahahahhah', 'ciaoooooooo', 'rosiconi', 'depositare', 'giustamente', 'capellone', 'nellarticolo', 'ahahahhahah', 'colta', 'girone', 'scavando', 'domandavo', 'eufemismo', 'perdenti', 'speac', 'dovrai', 'dobblig', 'pareva', 'purtoppo', 'capiva', 'disegnino', 'trivelliscono', 'decrepite', 'notevolmente', 'legitto', 'stiano', 'compenso', 'investigativi', 'sufficientemente', 'taccion', 'fueugenio', 'frequento', 'lavrebbe', 'letio', 'odisseo', 'ottuso', 'gonfiato', 'luminosa', 'volontarismo', 'bellarticol', 'rossana', 'imprenditore', 'trilly', 'xch', 'stavano', 'insaputa', 'speaches', 'grossa', 'simpatia', 'mantenendo', 'wister', 'vaticano', 'twittando', 'quousque', 'sospetto', 'copiano', 'daltronde', 'ipocrita', 'validi', 'injectorremover', 'extimated', 'outshin', 'investigazioni', 'estranea', 'averne', 'scioper', 'hackersno', 'originin'])

source_doc = 'exploit'
target_docs = ['cve', 'issue', 'discovered', 'hyland', 'onbase', 'directory', 'traversal', 'exists', 'reading', 'file', 'demonstrated', 'filename', 'parameter']

# This will return 3 target docs with similarity score

sim_scores = word_vectors.similarity(source_doc, target_docs)