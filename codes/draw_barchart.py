import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 베이스라인 모델 - Frequency, by BC, RF, Random grouping method

df = pd.read_csv('/Users/jungh/Downloads/PredictCyberAttacks/barchart/baseline_result.csv')
df = df.set_index('x')
df.columns.names=['Grouping Method']

colors=['lightblue','sandybrown','thistle']
plt.figure(figsize=(10,8))
df.plot(kind='bar',color=colors,linewidth=1,edgecolor='gray',alpha=0.8)
plt.rc('font', family='Times New Roman',size=15)
plt.axhline(y=50, color='lightgrey', linewidth=1)
#plt.title('Baseline Model: Tweet Frequency',fontweight="bold",size=25)
plt.xlabel('x days before cyberattack',size=20)
plt.xticks(rotation=0)
plt.ylabel('Prediction accuracy (%)',size=20)
plt.ylim([0, 100]) 
#plt.rcParams['figure.figsize'] = [10, 8]
plt.show()

#텍스트 유사도 측정 기준 도입에 따른 실험 결과
df = pd.read_csv('/Users/jungh/Downloads/PredictCyberAttacks/barchart/similarity_measure_evaluation.csv')
df = df.set_index('x')
df.columns.names=['Text Similarity Measures']

colors=['lightblue','sandybrown','thistle','darkseagreen']
plt.figure(figsize=(10,8))
df.plot(kind='bar',color=colors,linewidth=1,edgecolor='gray',alpha=0.7,figsize=(15,13))
plt.rc('font', family='Times New Roman',size=30)
plt.axhline(y=50, color='lightgrey', linewidth=1)
plt.xticks(rotation=0,size = 50)
plt.yticks(np.arange(0, 101, step=10), size = 40)
plt.xlabel('x days before cyberattack',size=50)
plt.ylabel('Prediction accuracy (%)',size=50)
plt.ylim([0, 100]) 
plt.legend(fontsize=35)
plt.show()
#plt.rcParams['figure.figsize'] = [10, 8]


#그룹 별 frequency, rake, word2vec, doc2vec 실험 결과
df = pd.read_csv('/Users/jungh/Downloads/PredictCyberAttacks/barchart/rake.csv')
df = df.set_index('Grouping Method')
colors=['lightblue','lightblue','lightblue','lightsalmon','lightsalmon','lightsalmon','lightsalmon']

plt.figure(figsize=(10,8))
plt.bar(df.index,df['Unnamed: 1'],color=colors,edgecolor='gray',alpha=0.6)
plt.rc('font', family='Times New Roman',size=15)
plt.axhline(y=50, color='lightgrey', linewidth=1)
plt.title('1 days before cyberattack')
plt.xticks(rotation=0,size = 20)
plt.ylabel('Prediction accuracy (%)',size=20)
plt.ylim([0, 100]) 
#plt.rcParams['figure.figsize'] = [10, 8]
plt.show()

#297 vs 273 vs 197의 예측 정확도 비교

df = pd.read_csv('/Users/jungh/Downloads/PredictCyberAttacks/barchart/userRangeComparison.csv')
df = df.set_index('Unnamed: 0')
colors=['lightblue','lightsalmon','thistle']
plt.figure(figsize=(10,8))
df.plot(kind='bar',color=colors,linewidth=1,edgecolor='gray',alpha=0.7,figsize=(15,13))
plt.rc('font', family='Times New Roman',size=18)
plt.axhline(y=50, color='lightgrey', linewidth=1)
plt.xlabel('Text Similarity Measure',size=30)
plt.xticks(rotation=0,size=20)
plt.ylabel('Prediction accuracy (%)',size=30)
plt.yticks(np.arange(0, 101, step=10), size = 25)
plt.ylim([0, 100]) 
plt.legend(fontsize=18)
plt.gcf().set_size_inches(10, 8)
plt.show()

# Rake with X days
df = pd.read_csv('/Users/jungh/Downloads/PredictCyberAttacks/barchart/rake_withXdays.csv') # 또는 fig5_b.csv
df = df.set_index('x days before cyberattack')
df.plot(kind='bar',color=colors,linewidth=1,edgecolor='gray',alpha=0.7,figsize=(15,13))
plt.rc('font', family='Times New Roman',size=30)
plt.axhline(y=50, color='lightgrey', linewidth=2)
plt.xticks(rotation=0,size = 30)
plt.yticks(np.arange(0, 101, step=10), size = 30)
plt.ylabel('Prediction accuracy (%)',size=50)
plt.xlabel('x days before cyberattack',size=50)
plt.ylim([0, 100]) 
plt.legend(fontsize=35)
plt.show()

# Sentiment

df = pd.read_csv('/Users/jungh/Downloads/PredictCyberAttacks/barchart/Sentiment.csv') # 또는 fig5_b.csv
df = df.set_index('Unnamed: 0')
colors=['tomato','steelblue']
df.columns.names=['Group']
plt.figure(figsize=(10,8))
df.transpose().plot(kind='bar',color=colors,linewidth=1,edgecolor='gray',alpha=0.7,figsize=(15,13))
plt.rc('font', family='Times New Roman',size=30)
plt.axhline(y=50, color='lightgrey', linewidth=1)
plt.xticks(rotation=0,size = 50)
plt.yticks(np.arange(0, 101, step=10), size = 40)
plt.xlabel('Group',size=50)
plt.ylabel('Sentiment Score',size=50)
plt.ylim([0, 100]) 
plt.legend(fontsize=35)
plt.show()


df = pd.read_csv('/Users/jungh/Downloads/PredictCyberAttacks/barchart/CSI_Relevance_Score.csv') # 또는 fig5_b.csv
df = df.set_index('Group')
colors=['lightblue','sandybrown','thistle','darkseagreen']
plt.figure(figsize=(10,8))
df.plot(kind='bar',color=colors,linewidth=1,edgecolor='gray',alpha=0.7,figsize=(15,13))
plt.rc('font', family='Times New Roman',size=30)
plt.axhline(y=50, color='lightgrey', linewidth=1)
plt.xticks(rotation=0,size = 50)
plt.yticks(np.arange(0, 5, step=1), size = 40)
plt.xlabel('Group',size=50)
plt.ylabel('CSI Relevance Score basde on Rake',size=50)
plt.ylim([0, 5]) 
plt.legend(fontsize=35)
plt.show()

simple = [2.602, 2.503, 2.889, 2.573]
simple.plot(kind='bar',color=colors,linewidth=1,edgecolor='gray',alpha=0.7,figsize=(15,13))

x = np.arange(4)
groups = ['1', '2', '3','4']
values =  [2.602, 2.503, 2.889, 2.573]

plt.bar(x, values,colors=['r','g','b','r'])
plt.xticks(x, groups)

plt.show()

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(4)
years = ['1', '2', '3', '4']
values = [2.602, 2.503, 2.889, 2.573]
colors = ['lightblue','sandybrown','thistle','darkseagreen']

plt.bar(x, values, color=colors,width = 0.5)
plt.xticks(x, years)
plt.xlabel('Group',size = 25)
plt.ylabel('Relevance Score',size = 25)
plt.yticks(np.arange(0, 6, step=1), size = 30)
plt.xticks(rotation=0,size = 30)
plt.rc('font', family='Times New Roman',size=15)


plt.show()

import matplotlib.pyplot as plt
ratio = [26.5,
26.08,
47.42
]
labels = ['Negative', 'Positive']
colors=['tomato','steelblue','yellowgreen']
plt.pie(ratio, autopct='%.1f%%', colors = colors, explode = [0.01,0.01,0.01])
plt.rc('font', family='Times New Roman',size=20)
plt.show()
