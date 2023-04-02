import os,json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta,date
from collections import Counter

def divide_by_year(groupNum):
    path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/gr'
    
    #groupNum = 4
    files = os.listdir(path+str(groupNum)+'_filtered')
    
    tw2017 = []
    tw2018 = []
    tw2019 = []
    
    # Divide By Year Using 'datetime' information
    for file in range(len(files)):
        jdata = open(path+str(groupNum)+'_filtered/'+str(files[file]), encoding="utf-8").read() 
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
    
    # Year 별, Group 별 Json file로 저장함
    path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/'
    
    with open(path+'year_filtered/2017/group'+str(groupNum)+'_2017.json','w') as makefile :
        json.dump(tw2017,makefile)
    with open(path+'year_filtered/2018/group'+str(groupNum)+'_2018.json','w') as makefile :
        json.dump(tw2018,makefile)
    with open(path+'year_filtered/2019/group'+str(groupNum)+'_2019.json','w') as makefile :
        json.dump(tw2019,makefile)
    
def calculate_freq(year,groupNum):
    
    path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/year_filtered/'
    jdata = open(path+str(year)+'/group'+str(groupNum)+'_'+str(year)+'.json', encoding="utf-8").read() 
    data = json.loads(jdata) 
    
    date_list = []
    
    for i in range(len(data)):
        date_list.append(data[i]['datetime'][0:10])
        
    freqDic = dict(Counter(date_list))
    
    freq = pd.DataFrame(freqDic.items(), columns=['Date', 'Frequency'])
    freq = freq.set_index('Date')
    freq['datetime'] = pd.to_datetime(freq.index)
    freq.sort_values(by='datetime',axis=0,inplace=True)
    freq = freq.drop('datetime',axis=1) #json으로 저장할 때 datetime이 자꾸 깨져서 일단
    #freq.set_index('datetime',inplace=True)
    
    df = freq.to_json()
    
    with open(path+str(year)+'/group'+str(groupNum)+'_freq.json','w') as makefile :
        json.dump(df,makefile)
    
def set_attack_date(year):
    path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019'

    with open(path+'/year_filtered/'+str(year)+'/attack_date.json','r') as atkfile:
        attack_date = json.load(atkfile)
    periodList = []
    
    for i in range(len(attack_date)):
        date = datetime.strptime(attack_date[i]['Attack'],"%Y-%m-%d")
        period = []
        for i in range(-5,1):
            period.append(str(date+timedelta(days=i))[0:10])
            #periodList.append(str(date+timedelta(days=i))[0:10])
        periodList.append(period)

    return periodList

# Recall 계산을 위해서 모든 날짜 리스트에 다 담음.
start = date(2019,1,6)
end = date(2019,12,31)
delta = end - start
dates = []
for i in range(delta.days+1):
    dates.append(start+timedelta(days=i))

periodList = []
    
for i in range(len(dates)):
    date = dates[i]
    period = []
    for i in range(-5,1):
        period.append(str(date+timedelta(days=i))[0:10])
    periodList.append(period)


def drawTimeSeries(year,groupNum):

    attackDate = set_attack_date(year)

    path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/year_filtered/'
    #jdata = open(path+str(year)+'/group'+str(groupNum)+'_w2v.json', encoding="utf-8").read() # 단순 트윗 개수
    jdata = open(path+str(year)+'/group'+str(groupNum)+'_w2v.json', encoding="utf-8").read() # Rake 
    data = json.loads(jdata) 
    data = dict(data[0])
    df = pd.DataFrame(data.items(),columns=['date','frequency'])
    df.date = pd.to_datetime(df.date)
    df.set_index('date',inplace=True)
    
    max_freq = df.frequency.max()
    min_freq = df.frequency.min()    
    
    df['freq_normalized']=(df['frequency']-min_freq)/(max_freq-min_freq)
    
    year_avg = df['freq_normalized'].mean()
    year_avg_list.append(year_avg)
    year_avg_list=[]
    period_avg_list=[[],[],[],[]]

    # 상위 25% 유저의 score정보
    # top_jdata = open(path+str(year)+'/group'+str(groupNum)+'_rake_top.json', encoding="utf-8").read() # Rake 
    # top_data = json.loads(top_jdata) 
    # top_data = dict(top_data[0])
    # top_df = pd.DataFrame(top_data.items(),columns=['date','frequency'])
    # top_df.date = pd.to_datetime(top_df.date)
    # top_df.set_index('date',inplace=True)
    
    # top_max_freq = top_df.frequency.max()
    # top_min_freq = top_df.frequency.min()    
    
    # top_df['freq_normalized']=(top_df['frequency']-top_min_freq)/(top_max_freq-top_min_freq)
    
    # top_year_avg = top_df['freq_normalized'].mean()
    # top_year_avg_list.append(top_year_avg)    

    for i in range(1,len(attackDate)+1):
        period_avg = sum(df.loc[attackDate[i-1]]['freq_normalized'].tolist())/len(df.loc[attackDate[i-1]]['freq_normalized'].tolist())
        period_avg_list[groupNum-1].append(period_avg)
        
        # top_period_avg = sum(top_df.loc[attackDate[i-1]]['freq_normalized'].tolist())/len(top_df.loc[attackDate[i-1]]['freq_normalized'].tolist())
        # top_period_avg_list[groupNum-1].append(top_period_avg)
        
        plt.figure(figsize=(10, 5))
        # plt.title('Top 25% User Rake-nltk')

        plt.plot(attackDate[i-1],df.loc[attackDate[i-1]]['freq_normalized'].tolist(),color='black', marker='o',linestyle='solid')
        plt.plot(attackDate[i-1],[year_avg]*len(attackDate[i-1]),color='green',linestyle='solid',label='Year Average')
        plt.plot(attackDate[i-1],[period_avg]*len(attackDate[i-1]),color='red',linestyle='solid',label='Period Average')
        
        #plt.plot(attackDate[i-1],top_df.loc[attackDate[i-1]]['freq_normalized'].tolist(),color='black', marker='o',linestyle='solid')
        #plt.plot(attackDate[i-1],[top_year_avg]*len(attackDate[i-1]),color='green',linestyle='solid',label='Year Average')
        #plt.plot(attackDate[i-1],[top_period_avg]*len(attackDate[i-1]),color='red',linestyle='solid',label='Period Average')
        plt.legend()
        # plt.savefig(path+'final_graph/'+str(year)+'/group'+str(groupNum)+'_'+attackDate[i-1][3]+'_rake.png')

# 연도별로 있는 groupN_processed 파일 합쳐서 각 rake/w2v score의 상위 25%에 속하는 user list 계산해서 return하는 함수
def CreateTopUserList(groupNum):
    path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/year_filtered/'
    data2017 = open(path+str(2017)+'/group'+str(groupNum)+'_processed.json', encoding="utf-8").read()
    data2018 = open(path+str(2018)+'/group'+str(groupNum)+'_processed.json', encoding="utf-8").read()    
    data2019 = open(path+str(2019)+'/group'+str(groupNum)+'_processed.json', encoding="utf-8").read()
    data2017 = json.loads(data2017)
    data2018 = json.loads(data2018)
    data2019 = json.loads(data2019)
    data = data2017+data2018+data2019

    df = pd.DataFrame(data)
    df.drop(['ID', 'text','text_processed','has_media', 'medias'],axis=1,inplace=True)
    groupby = df.groupby('usernameTweet').mean()
    count = df.groupby('usernameTweet').count()
    count.drop(['datetime', 'rake_score'],axis=1,inplace=True)
    count.rename(columns = {'w2v_score' : 'count'}, inplace = True)
    groupby = pd.merge(groupby, count, on='usernameTweet')
    rake_sort = groupby.sort_values(by='rake_score',ascending=False).drop(['w2v_score'],axis=1)
    w2v_sort = groupby.sort_values(by='w2v_score',ascending=False).drop(['rake_score'],axis=1)
    
    rakeTopUser = []
    w2vTopUser = []
    for i in range(len(rake_sort)):
        if rake_sort['count'][i]>10:
            rakeTopUser.append(rake_sort.index[i])
        if len(rakeTopUser)==round(0.25*len(rake_sort)):
            break
        
    for i in range(len(w2v_sort)):
        if w2v_sort['count'][i]>10:
            w2vTopUser.append(w2v_sort.index[i])
        if len(w2vTopUser)==round(0.25*len(w2v_sort)):
            break
    
    return [rakeTopUser,w2vTopUser]

# 상위 25%유저 리스트 받아와서 그들의 트윗만 남겨서 {'datetime':'score'} json file로 저장
def drawOnlyTopUser(year,groupNum):
    path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/year_filtered/'
    jdata = open(path+str(year)+'/group'+str(groupNum)+'_processed.json', encoding="utf-8").read()
    data = json.loads(jdata)
    
    rakeTopUser = CreateTopUserList(groupNum)[0]
    w2vTopUser = CreateTopUserList(groupNum)[1]

    temp = []
    for i in range(len(data)):
        if data[i]['usernameTweet'] in rakeTopUser:
            temp.append(data[i])
    df = pd.DataFrame(temp)
    df.drop(['ID', 'text','has_media', 'medias'],axis=1,inplace=True)
    df_mean = df.groupby('datetime').mean()
    
    rake = df_mean['rake_score'].to_json()
    with open(path+str(year)+'/group'+str(groupNum)+'_rake_top.json','w') as makefile :
        json.dump(rake,makefile)
    
    temp = []
    for i in range(len(data)):
        if data[i]['usernameTweet'] in w2vTopUser:
            temp.append(data[i])
    df = pd.DataFrame(temp)
    df.drop(['ID', 'text','has_media', 'medias'],axis=1,inplace=True)
    df_mean = df.groupby('datetime').mean()
    
    w2v = df_mean['w2v_score'].to_json()
    with open(path+str(year)+'/group'+str(groupNum)+'_w2v_top.json','w') as makefile :
        json.dump(w2v,makefile)

if __name__ == '__main__':
    divide_by_year(1)
    divide_by_year(2)
    divide_by_year(3)
    divide_by_year(4)
    
    calculate_freq(2017,1)
    calculate_freq(2018,1)
    calculate_freq(2019,1)
    calculate_freq(2017,2)
    calculate_freq(2018,2)
    calculate_freq(2019,2)
    calculate_freq(2017,3)
    calculate_freq(2018,3)
    calculate_freq(2019,3)
    calculate_freq(2017,4)
    calculate_freq(2018,4)
    calculate_freq(2019,4)
    
    
    top_year_avg_list = []
    top_period_avg_list = [[],[],[],[]]
    year_avg_list = []
    period_avg_list = [[],[],[],[]]
    drawTimeSeries(2017,1)
    drawTimeSeries(2017,2)
    drawTimeSeries(2017,3)
    drawTimeSeries(2017,4)

    year_avg_list = []
    period_avg_list = [[],[],[],[]]
    drawTimeSeries(2018,1)
    drawTimeSeries(2018,2)
    drawTimeSeries(2018,3)
    drawTimeSeries(2018,4)

    year_avg_list = []
    period_avg_list = [[],[],[],[]]
    drawTimeSeries(2019,1)
    drawTimeSeries(2019,2)
    drawTimeSeries(2019,3)
    drawTimeSeries(2019,4)

