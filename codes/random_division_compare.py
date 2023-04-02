import os
import random
import json
import pandas as pd
import numpy as np

path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/group'

allUser = list(merge_all['usernameTweet'].unique())

# 전체 유저 197명을, 랜덤하게 30명씩 4개의 그룹으로 나눈다

out1 = random.sample(allUser,27)

print(out1)

for i in range(len(out1)):
    allUser.remove(out1[i])
    
out2 = random.sample(allUser,27)

for i in range(len(out2)):
    allUser.remove(out2[i])

print(out2)    
    
out3 = random.sample(allUser,27)

for i in range(len(out3)):
    allUser.remove(out3[i])
    
print(out3)

out4 = random.sample(allUser,27)

for i in range(len(out4)):
    allUser.remove(out4[i])
    
print(out4)

# 기존에 그룹별로 계산해놨던 Rake Score를 사용하자

group1Rake = []
group2Rake = []
group3Rake = []
group4Rake = []

groupNum = 4

path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/year_filtered/'
jdata = open(path+str(2017)+'/30/group'+str(groupNum)+'_processed_30.json', encoding="utf-8").read() 
data = json.loads(jdata)
df2017 = pd.DataFrame(data)
df2017 = df2017.drop(columns=['ID', 'text', 'text_processed', 'w2v_score', 'has_media', 'medias'], axis=1)

for d in range(len(df2017)):
    if df2017['datetime'][d] in attack2017: # 공격기간에 속하는 것만 남기기
        group4Rake.append(df2017['rake_score'][d])

#df2017 = df2017.groupby(df2017['usernameTweet']).mean() # Sum할까 Mean할까

jdata = open(path+str(2018)+'/30/group'+str(groupNum)+'_processed_30.json', encoding="utf-8").read() 
data = json.loads(jdata) 
df2018 = pd.DataFrame(data)
df2018 = df2018.drop(columns=['ID', 'text', 'text_processed', 'w2v_score', 'has_media', 'medias'], axis=1)
#df2018 = df2018.groupby(df2018['usernameTweet']).mean()

for d in range(len(df2018)):
    if df2018['datetime'][d] in attack2018: # 공격기간에 속하는 것만 남기기
        group4Rake.append(df2018['rake_score'][d])

jdata = open(path+str(2019)+'/30/group'+str(groupNum)+'_processed_30.json', encoding="utf-8").read() 
data = json.loads(jdata) 
df2019 = pd.DataFrame(data)
df2019 = df2019.drop(columns=['ID', 'text', 'text_processed', 'w2v_score', 'has_media', 'medias'], axis=1)
#df2019 = df2019.groupby(df2019['usernameTweet']).mean()

for d in range(len(df2019)):
    if df2019['datetime'][d] in attack2019: # 공격기간에 속하는 것만 남기기
        group4Rake.append(df2019['rake_score'][d])

group4Rake_ = [0]*len(group4Rake)
for i in range(len(group4Rake)):
    group4Rake_[i] = (group4Rake[i]-0.0)/(17.0-0.0)

merge1 = pd.concat([df2017, df2018,df2019]).groupby(['datetime','usernameTweet']).mean().reset_index() # Gr1 유저의 Rake_score. 연도 합친거.
merge2 = pd.concat([df2017, df2018,df2019]).groupby(['datetime','usernameTweet']).mean().reset_index() # Gr2 유저의 Rake_score. 
merge3 = pd.concat([df2017, df2018,df2019]).groupby(['datetime','usernameTweet']).mean().reset_index() # Gr3 유저의 Rake_score. 
merge4 = pd.concat([df2017, df2018,df2019]).groupby(['datetime','usernameTweet']).mean().reset_index() # Gr4 유저의 Rake_score. = pd.concat([merge1,merge2,merge3,merge4]).reset_index() # 전체 유저 합친거
merge_all = pd.concat([merge1,merge2,merge3,merge4]).reset_index()

# MinMax 정규화
minV = merge_all['rake_score'].min()
maxV = merge_all['rake_score'].max()
merge_all['rake_normalize'] = None


for i in range(len(merge_all)):
    merge_all['rake_normalize'] = (merge_all['rake_score'] - minV) / (maxV - minV)


     
np.std([merge1['rake_score'].mean(), merge2['rake_score'].mean(), merge3['rake_score'].mean(), merge4['rake_score'].mean()])
np.std([merge1['rake_normalize'].mean(), merge2['rake_normalize'].mean(), merge3['rake_normalize'].mean(), merge4['rake_normalize'].mean()])

random1 = []
random2 = []
random3 = []
random4 = []
count = 0
for i in range(len(merge_all)):
    if merge_all['usernameTweet'][i] in out1 and merge_all['datetime'][i] in attacks:
        random1.append(merge_all['rake_score'][i])
        count+=1
    elif merge_all['usernameTweet'][i] in out2 and merge_all['datetime'][i] in attacks:
        random2.append(merge_all['rake_score'][i])
        count+=1
    elif merge_all['usernameTweet'][i] in out3 and merge_all['datetime'][i] in attacks:
        random3.append(merge_all['rake_score'][i])
        count+=1
    elif merge_all['usernameTweet'][i] in out4 and merge_all['datetime'][i] in attacks:
        random4.append(merge_all['rake_score'][i])
        count+=1
        
np.std([np.mean(random1),np.mean(random2),np.mean(random3),np.mean(random4)])

wannaCry_freq_cd = [0,0,0,0]
wannaCry_freq_ran = [0,0,0,0]
year_freq_ran = [0,0,0,0]

for i in range(len(df2017_all)):
    if df2017_all['usernameTweet'][i] in out1:
        year_freq_ran[0]+=1
        if df2017_all['datetime'][i] in WannaCry:
            wannaCry_freq_ran[0]+=1
    elif df2017_all['usernameTweet'][i] in out2:
        year_freq_ran[1]+=1
        if df2017_all['datetime'][i] in WannaCry:
            wannaCry_freq_ran[1]+=1
    elif df2017_all['usernameTweet'][i] in out3:
        year_freq_ran[2]+=1
        if df2017_all['datetime'][i] in WannaCry:
            wannaCry_freq_ran[2]+=1
    elif df2017_all['usernameTweet'][i] in out4:
        year_freq_ran[3]+=1
        if df2017_all['datetime'][i] in WannaCry:
            wannaCry_freq_ran[3]+=1
            
np.std(year_freq_ran)
np.std(wannaCry_freq_cd)


df2017 = df2017.drop(columns=['ID', 'text', 'text_processed', 'w2v_score', 'has_media', 'medias'], axis=1)
df2017_all = pd.concat([df2017, df2017_all])

len(df2017)/len(df2017['usernameTweet'].unique())

for i in range(len(df2017_4)):
    if df2017_4['datetime'][i] in WannaCry:
        wannaCry_freq_cd[3] += 1