import pandas as pd
import numpy as np
from py2neo import Graph
import json

def grouping():
    #neo4j의 Community Detection - Louvain Algorithm을 적용한 결과 파일 (.csv)
    data = pd.read_csv('/Users/jungh/Desktop/export.csv')

    # gr1,gr2,gr3,gr4 = [],[],[],[]

    # for i in range(len(data)):
    #     cid = str(data['communityId'][i]).strip()
    #     if cid == '128':
    #         gr1.append(data['username'][i].strip())
    #     elif cid == '135':
    #         gr2.append(data['username'][i].strip())
    #     elif cid == '221':
    #         gr3.append(data['username'][i].strip())
    #     elif cid == '238':
    #         gr4.append(data['username'][i].strip())
    #     else:
    #         pass
    
    # result = [gr1, gr2, gr3, gr4]
    # return result

    #username과 communityId 2가지 column으로 이루어짐.
    username = data['username'].tolist()
    communityId = data['communityId'].tolist()

    li = []
    for i in range(len(data['communityId'].unique())):
        c = communityId.count(data['communityId'].unique()[i])
        li.append(c)

    ind = []
    for i in range(len(li)):
        if (li[i]>45):
            ind.append(i)

    frequentId = []
    for j in range(len(ind)):
        frequentId.append(data['communityId'].unique()[ind[j]])


    result = []
    for n in range(len(frequentId)):
        c1 = []
        for k in range(len(data)):
            if (data['communityId'][k] == frequentId[n]):
                c1.append(data['username'][k].strip())
        result.append(c1)

    return result

def extract_relation(result):
    json_data=open('/Users/jungh/Downloads/PredictCyberAttacks/Crawling/Follow/1000/Relationship_300.json').read()
    data = json.loads(json_data)
    gr1, gr2, gr3, gr4 = result[0],result[1],result[2],result[3]
    gr1 = [line.strip() for line in gr1]
    gr2 = [line.strip() for line in gr2]
    gr3 = [line.strip() for line in gr3]
    gr4 = [line.strip() for line in gr4]
    data_gr1,data_gr2,data_gr3,data_gr4 = [],[],[],[]

    for i in range(len(data)):
        user = str(data[i]['username'])
        if user.strip() in gr1:
            data_gr1.append(data[i])
        elif user.strip() in gr2:
            data_gr2.append(data[i])
        elif user.strip() in gr3:
            data_gr3.append(data[i])
        elif user.strip() in gr4:
            data_gr4.append(data[i])
        else:
            pass

    #  128, 135, 221, 238 - 결과 json으로 저장하기
    with open('/Users/jungh/Desktop/group1.json','w') as towrite:
        json.dump(data_gr1,towrite,ensure_ascii=False)

    with open('/Users/jungh/Desktop/group2.json','w') as towrite:
        json.dump(data_gr2,towrite,ensure_ascii=False)

    with open('/Users/jungh/Desktop/group3.json','w') as towrite:
        json.dump(data_gr3,towrite,ensure_ascii=False)

    with open('/Users/jungh/Desktop/group4.json','w') as towrite:
        json.dump(data_gr4,towrite,ensure_ascii=False)

def create_node(result):
    #Neo4j에다가 Node 생성
    groupName = ['zero','one','two','three','four']
    graph.delete_all()
    for i in range(1,5):
        j = i-1
        json_data=open('/Users/jungh/Desktop/group'+str(i)+'.json').read()
        jdata = json.loads(json_data)
        for k in range(len(result[j])):
            graph.run('create (u:'+groupName[i]+' {username:"'+str(result[j][k])+'"})')

def create_rel():
    #Neo4j에 Relationship 저장
    groupName = ['zero','one','two','three','four']
    for k in range(1,5):
        json_data=open('/Users/jungh/Desktop/group'+str(k)+'.json').read()
        jdata = json.loads(json_data)

        for i in range(0,len(jdata)):
            for n in range(0,len(jdata[i]['following'])):
                graph.run("match (a:"+groupName[k]+"),(b:"+groupName[k]+") "+"where a.username='"+str(jdata[i]['username'])+"' and b.username='"+str(jdata[i]['following'][n])+"' "+"merge (a)-[:follow]->(b)")  

        for i in range(0,len(jdata)):
            for n in range(0,len(jdata[i]['follower'])):
                graph.run("match (a:"+groupName[k]+"),(b:"+groupName[k]+") "+"where a.username='"+str(jdata[i]['username'])+"' and b.username='"+str(jdata[i]['follower'][n])+"' "+"merge (b)-[:follow]->(a)")  

if __name__ == '__main__':

    result = grouping()
    extract_relation(result)

    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "1234"     
    graph = Graph(uri=uri, user=user, password=password)
    create_node(result)
    create_rel()