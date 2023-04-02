import os,json
import pandas as pd

files = os.listdir('/Users/jungh/Desktop/getTweetText/gr2_processed')
df = []
document = []
for i in range(len(files)): #GroupN에 속하는 User들 모두 순회
    jdata = open("/Users/jungh/Desktop/getTweetText/gr2_processed/"+str(files[i]), encoding="utf-8").read() #한 유저 파일 접근
    data = json.loads(jdata)  
    print(str(files[i]).split('.')[0]) #프린트
    if (data == []): #data가 빈 데이터면 다음사람으로 넘어가자
        continue
    for j in range(len(data)): #user데이터에서 모든 tweet text 순회
        document.append(data[j]['text'])
    
with open('/Users/jungh/Desktop/getTweetText/gr2corpus.txt', 'w') as f:
    for item in document:
        f.write("%s\n" % item)
        