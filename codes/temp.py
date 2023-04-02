import json
import tweepy           # To consume Twitter's API
import pandas as pd     # To handle data
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


# Consumer API keys:
CONSUMER_KEY = "4oqZjge7qM0n3WNftJiKHFtOF" #API key
CONSUMER_SECRET = "CZOzvRcdwFOzPZFoM5igXVGBbOBp7lQWBBtCRe76wuv738equP" 
ACCESS_TOKEN = "1004411169568747520-7NBYDlDKlGXX9q5gjXasgRRo5p3HtT" 
ACCESS_TOKEN_SECRET = "b3BSPhEfHGYCxuIaNPg1CFcJtKkCWnjIZESooDgT99GWL" 


# Authentication and access using keys:

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_delay=10)

accountlist = pd.read_csv('/Users/jungh/Desktop/BC_export.csv')
values = list(accountlist['screen_name'].values)
accountlist['screen_name']=None


for i in range(len(accountlist)):
    try:
        accountlist['screen_name'][i]=api.get_user(accountlist['username'][i]).screen_name
    except:
        accountlist['screen_name'][i] = None
        
    print(i)
    
accountlist.to_csv("/Users/jungh/Desktop/BC_export.csv",encoding="utf-8")


#Random User Generate
import numpy as np
np_array=np.array(values)
np.random.shuffle(np_array)
j = -1
for i in range(len(np_array)):
    j += 1
    if np_array[j] == 'nan' :
        np_array = np.delete(np_array, j)
        j -= 1
BC_user = list(np_array[0:50])        
random_user = list(np.random.choice(np_array, size=50, replace=False))

for i in range(len(random_user)):
    random_user[i] = str(random_user[i])

import os,shutil
path = '/Users/jungh/Downloads/PredictCyberAttacks/All Tweets/Tweet_2019'
files = os.listdir(path)

for i in range(len(files)):
    if files[i].split(".")[0] in user226:
        shutil.copy2('C:/Users/jungh/Downloads/PredictCyberAttacks/All Tweets/Tweet_2019/'+files[i], 'C:/Users/jungh/Downloads/PredictCyberAttacks/All Tweets/226')

def divide_by_year(groupNum):
    path = '/Users/jungh/Downloads/PredictCyberAttacks/All Tweets/226/'
    
    #groupNum = 4
    files = os.listdir(path)
    
    tw2017 = []
    tw2018 = []
    tw2019 = []
    
    # Divide By Year Using 'datetime' information
    for file in range(len(files)):
        jdata = open(path+str(files[file]), encoding="utf-8").read() 
        data = json.loads(jdata) 
    
        for i in data[:]:
            if (i['datetime'][0:4] == '2017'):
                tw2017.append(i)
                continue
            elif (i['datetime'][0:4] == '2018'):
                tw2018.append(i)
                continue
            elif (i['datetime'][0:4] == '2019'):
                tw2019.append(i)
                continue
            
        print(file, str(files[file]))
    
    with open(path+'2017.json','w') as makefile :
        json.dump(tw2017,makefile)
    with open(path+'2018.json','w') as makefile :
        json.dump(tw2018,makefile)
    with open(path+'2019.json','w') as makefile :
        json.dump(tw2019,makefile)
    
# Text Preprocessing!! 
path = '/Users/jungh/Downloads/PredictCyberAttacks/All Tweets/262/'
files = os.listdir(path)
for i in range(len(files)):
    print(str(files[i])+" Processing...")
    jdata = open(path+str(files[i]),encoding="utf-8").read() #해당 user에 대한 모든 text가 들어있는 json file
    data = json.loads(jdata)
    for j in range(len(data)):
        if data[j]:
            data[j]['text'] = textCleaning(data[j]['text']) #text 하나하나에 대해서 cleaning 하고, corpus에 추가
    with open('/Users/jungh/Downloads/PredictCyberAttacks/All Tweets/262_processed/'+str(files[i]), 'w', encoding='utf-8') as make_file:
        json.dump(data,make_file) #변환된 text를 저장 user한명당 하나의 파일로 저장함
        print("Done!")
        
def calculate_freq(year,groupNum):
    
    path = '/Users/jungh/Downloads/PredictCyberAttacks/All Tweets/all_user_processed/'
    jdata = open(path+str(year)+'.json', encoding="utf-8").read() 
    data = json.loads(jdata) 
    
    date_list = []
    
    for i in range(len(corpus)):
        date_list.append(corpus[i]['datetime'][0:10])
        
    freqDic = dict(Counter(date_list))
    
    freq = pd.DataFrame(freqDic.items(), columns=['Date', 'Frequency'])
    freq = freq.set_index('Date')
    freq['datetime'] = pd.to_datetime(freq.index)
    freq.sort_values(by='datetime',axis=0,inplace=True)
    freq = freq.drop('datetime',axis=1) #json으로 저장할 때 datetime이 자꾸 깨져서 일단
    #freq.set_index('datetime',inplace=True)
    
    df = freq.to_json()
    
    with open(path+str(year)+'_filtered_freq.json','w') as makefile :
        json.dump(df,makefile)

attackDate = set_attack_date(2018) 
path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/year_filtered/'

threshold = 0.0

from collections import defaultdict

def drawTimeSeries(year,groupNum):

    attackDate = set_attack_date(year)

    jdata = open(path+str(2019)+'/30/group'+str(3)+'_rake_30.json', encoding="utf-8").read() 
    data = json.loads(jdata) 
    data = dict(data[0])
    df = pd.DataFrame(data.items(),columns=['date','frequency'])
    df.date = pd.to_datetime(df.date)
    df.set_index('date',inplace=True)
    
    max_freq = df.frequency.max()
    min_freq = df.frequency.min()
    
    df['freq_normalized']=(df['frequency']-min_freq)/(max_freq-min_freq) # 정규화
        
    ###################################################################################
    year_avg = df['freq_normalized'].mean()
    
    relevancy = defaultdict(bool)
    # diff = []
    
    for i in range(len(periodList)):
        period_avg = sum(df.loc[periodList[i-1]]['freq_normalized'].tolist())/len(df.loc[periodList[i-1]]['freq_normalized'].tolist())
        
        #diff.append(period_avg - year_avg)
        
    #diff_total[year][groupNum-1].append(diff)     
    
        if period_avg - year_avg > threshold :
            relevancy[periodList[i][5]] = True
        else:
            relevancy[periodList[i][5]] = False
         
    count=0
    for k in range(len(list(relevancy.values()))):
        if list(relevancy.values())[k]==True:
            count+=1
    print(count)

year_avg_total = {2017:[[],[],[],[]], 2018:[[],[],[],[]], 2019:[[],[],[],[]]} # 연도별 - 그룹별 - 메져별
period_avg_total = {2017:[[],[],[],[]], 2018:[[],[],[],[]], 2019:[[],[],[],[]]}

diff_total = {2017:[[],[],[],[]], 2018:[[],[],[],[]], 2019:[[],[],[],[]]}

std_total = {2017:[[],[],[],[]], 2018:[[],[],[],[]], 2019:[[],[],[],[]]}
mean_total = {2017:[[],[],[],[]], 2018:[[],[],[],[]], 2019:[[],[],[],[]]}

years = [2017,2018,2019]

for year in years:
    for gr in range(4):
        for m in range(3):
            mean_total[year][gr].append(np.mean([item for item in diff_total[year][gr][m] if item > 0]))


year_avg_total[year][groupNum-1].append(df['freq_normalized'].mean())
    
drawTimeSeries(2017)
drawTimeSeries(2018)
drawTimeSeries(2019)

drawTimeSeries(2017,1)
drawTimeSeries(2017,2)
drawTimeSeries(2017,3)
drawTimeSeries(2017,4)
drawTimeSeries(2018,1)
drawTimeSeries(2018,2)
drawTimeSeries(2018,3)
drawTimeSeries(2018,4)
drawTimeSeries(2019,1)
drawTimeSeries(2019,2)
drawTimeSeries(2019,3)
drawTimeSeries(2019,4)    
    
 # 전체 user에 대하여 rake, word2vec 적용한 결과 도출   
def calculate_score(year):
    
    path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/year_filtered/'
    jdata = open(path+str(year)+'/group1_processed.json', encoding="utf-8").read() 
    data1 = json.loads(jdata) 
    jdata = open(path+str(year)+'/group2_processed.json', encoding="utf-8").read() 
    data2 = json.loads(jdata) 
    jdata = open(path+str(year)+'/group3_processed.json', encoding="utf-8").read() 
    data3 = json.loads(jdata) 
    jdata = open(path+str(year)+'/group4_processed.json', encoding="utf-8").read() 
    data4 = json.loads(jdata) 
    data = data1+data2+data3+data4
    
    df = pd.DataFrame(data)
    df_mean = df.groupby('datetime').mean()
    rake = df_mean['rake_score'].to_json()
    w2v = df_mean['w2v_score'].to_json()
    
    with open(path+str(year)+'/group'+str(groupNum)+'_processed'+'.json','w') as makefile :
        json.dump(data,makefile)
    with open(path+str(year)+'/allUser_rake.json','w') as makefile :
        json.dump(rake,makefile)
    with open(path+str(year)+'/allUser_w2v.json','w') as makefile :
        json.dump(w2v,makefile)