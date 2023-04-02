from gensim.models.doc2vec import Doc2Vec
import json 
import pandas as pd 

model="C:/Users/jungh/Downloads/PredictCyberAttacks/doc2vec_model/doc2vec.bin"  #point to downloaded pre-trained doc2vec model

#load model
m = Doc2Vec.load(model)

keywordList = getKeyword() 

# keywordVector = m.infer_vector(keywordList)
# docVector = m.infer_vector(doc_words2)
# print(m.similarity(keywordVector, docVector))
#m.docvecs.similarity_unseen_docs(m,keywordList, doc_words2)

path = '/Users/jungh/Downloads/PredictCyberAttacks/All Tweets/226/'
year=2017
groupNum=1
def calculateD2V(year):
    jdata = open(path+str(year)+'_processed.json').read()
    data=json.loads(jdata)  
    
    df = pd.DataFrame(data)
    df = df.groupby('datetime').sum() #Datetime으로 Groupby
    df['docs']=df.apply(lambda x: [], axis=1) #Document를 담을 빈리스트 생성
    df.drop(['rake_score', 'w2v_score'],axis=1,inplace=True) # 안쓰이는 Columns삭제
    df['d2v score']=0.00 #Float Type으로 선언
    
    #날짜별로 묶어서 Docs에 추가하기 df의 형태 {날짜: [그 날짜에 쓰여진 모든 트윗 txt의 word 단위로 split한 리스트] }
    for i in range(len(data)):
        df.loc[data[i]['datetime']]['docs'].extend(data[i]['text_processed'].split())
    
    #날짜별로 그 날짜에 쓰여진 트윗 Documents와 RF KeywordList의 유사도를 구하여 df에 'd2v score' column에 추가    
    for i in range(len(df)):
        df['d2v score'][i] = float(m.docvecs.similarity_unseen_docs(m, df['docs'][i],keywordList))
        print(i)
        
    d2v = df['d2v score'].to_json() #JSON file로 변환
        
    # with open(path+str(year)+'/group'+str(groupNum)+'_d2v'+'.json','w') as makefile :
    #     json.dump(d2v,makefile) # 파일에 저장
    
    with open(path+str(year)+'_d2v.json','w') as makefile :
        json.dump(d2v,makefile) # 파일에 저장
calculateD2V(2018)
calculateD2V(2019)


calculateD2V(2017,1)
calculateD2V(2017,2)        
calculateD2V(2017,3)
calculateD2V(2017,4)

calculateD2V(2018,1)
calculateD2V(2018,2)
calculateD2V(2018,3)
calculateD2V(2018,4)

calculateD2V(2019,1)
calculateD2V(2019,2)
calculateD2V(2019,3)
calculateD2V(2019,4)