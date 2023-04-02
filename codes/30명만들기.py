import json,os
import pandas as pd

path = '/Users/jungh/Downloads/PredictCyberAttacks/All Tweets/random_user/' 
files=os.listdir(path)
for i in range(len(files)):
    files[i]=files[i].split('.')[0]

year=2019
jdata = open(path+'results/'+str(year)+'_processed.json', encoding="utf-8").read() 
data = json.loads(jdata) 

users=[]
for i in range(len(data)):
    if data[i]['usernameTweet'] in files:
        users.append(data[i])

name = []     
for i in range(len(users)):
    name.append(users[i]['usernameTweet'])
name = list(set(name))

df = pd.DataFrame(users)
df_mean = df.groupby('datetime').mean()
rake = df_mean['rake_score'].to_json()
w2v = df_mean['w2v_score'].to_json()
    
with open(path+str(year)+'_processed_30'+'.json','w') as makefile :
    json.dump(users,makefile)
with open(path+str(year)+'_rake_30.json','w') as makefile :
    json.dump(rake,makefile)
with open(path+str(year)+'_w2v_30.json','w') as makefile :
    json.dump(w2v,makefile)
    
# Proposed Method
import numpy as np

groupNum=4

path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/group'+str(groupNum)+'/'
files=os.listdir(path)
for i in range(len(files)):
    files[i]=files[i].split('.')[0]
random30 = list(np.random.choice(files, size=30, replace=False))
for i in range(len(random30)):
    random30[i] = str(random30[i])

year=2019
path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/year_filtered/'+str(year)+'/'
jdata = open(path+'group'+str(groupNum)+'_processed.json', encoding="utf-8").read() 
data = json.loads(jdata) 

users=[]
for i in range(len(data)):
    if data[i]['usernameTweet'] in random30:
        users.append(data[i])

name = []     
for i in range(len(users)):
    name.append(users[i]['usernameTweet'])
name = list(set(name))

df = pd.DataFrame(users)
df_mean = df.groupby('datetime').mean()
rake = df_mean['rake_score'].to_json()
w2v = df_mean['w2v_score'].to_json()
    
with open(path+'30/group'+str(groupNum)+'_processed_30'+'.json','w') as makefile :
    json.dump(users,makefile)
with open(path+'30/group'+str(groupNum)+'_rake_30.json','w') as makefile :
    json.dump(rake,makefile)
with open(path+'30/group'+str(groupNum)+'_w2v_30.json','w') as makefile :
    json.dump(w2v,makefile)
