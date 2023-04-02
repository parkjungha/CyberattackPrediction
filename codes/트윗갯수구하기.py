import os
import json

count = 0

path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/group1/'
files = os.listdir(path)
for i in range(len(files)):
    jdata = open(path+files[i], encoding="utf-8").read() 
    data = json.loads(jdata) 
    count += len(data)
    print(i)

path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/group2/'
files = os.listdir(path)
for i in range(len(files)):
    jdata = open(path+files[i], encoding="utf-8").read() 
    data = json.loads(jdata) 
    count += len(data)
    print(i)

path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/group3/'
files = os.listdir(path)
for i in range(len(files)):
    jdata = open(path+files[i], encoding="utf-8").read() 
    data = json.loads(jdata) 
    count += len(data)
    print(i)

path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/group4/'
files = os.listdir(path)
for i in range(len(files)):
    jdata = open(path+files[i], encoding="utf-8").read() 
    data = json.loads(jdata) 
    count += len(data)
    print(i)


print(count)
