import json
import os
import pandas as pd

path = "/Users/jungh/Downloads/PredictCyberAttacks/All Tweets/226/"
files = os.listdir(path)
​
#도대체 뭔 에러야 이게 

for i in range(len(files)):
    f = open(path+files[i], "r", encoding='utf-8')

    data= f.read()
​
    tweet = '['+data.replace('\n','').replace('}{','},{')+']'
​
    result  = json.loads(tweet)
​
    with open(path+files[i],'w',encoding='utf-8') as towrite:
        json.dump(result,towrite,ensure_ascii=False)
        
# group4에 wugeej 파일 열면 위험하다고 자꾸 에러남. 그래서 뺴고함 <이 프로그램은 위험하며 다른 프로그램을 다운로드합니다.>
# <OSError: [Errno 22] Invalid argument: '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/gr4/wugeej.json'>
        