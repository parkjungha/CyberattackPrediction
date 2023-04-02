from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import json
import matplotlib.pyplot as plt

def count_values_in_column(data,feature):
    total=data.loc[:,feature].value_counts(dropna=False)
    percentage=round(data.loc[:,feature].value_counts(dropna=False,normalize=True)*100,2)
    return pd.concat([total,percentage],axis=1,keys=['Total','Percentage'])

path = '/Users/jungh/Downloads/PredictCyberAttacks/Tweet_2019/year_filtered/'
jdata = open(path+str(2017)+'/30/group'+str(4)+'_processed_30.json', encoding="utf-8").read() 
data = json.loads(jdata) 
df2017 = pd.DataFrame(data)
df2017 = df2017.drop(columns=['ID', 'w2v_score', 'has_media', 'medias'], axis=1)

jdata = open(path+str(2018)+'/30/group'+str(4)+'_processed_30.json', encoding="utf-8").read() 
data = json.loads(jdata) 
df2018 = pd.DataFrame(data)
df2018 = df2018.drop(columns=['ID', 'rake_score', 'w2v_score', 'has_media', 'medias'], axis=1)

jdata = open(path+str(2019)+'/30/group'+str(4)+'_processed_30.json', encoding="utf-8").read() 
data = json.loads(jdata) 
df2019 = pd.DataFrame(data)
df2019 = df2019.drop(columns=['ID', 'w2v_score', 'has_media', 'medias'], axis=1)

concat_gr1 = pd.concat([df2017,df2018,df2019],ignore_index=True)

# 빈 데이터 프레임 만들기
group1 = pd.DataFrame(columns=['usernameTweet', 'text', 'datetime'])
group2 = pd.DataFrame(columns=['usernameTweet', 'text', 'datetime'])
group3 = pd.DataFrame(columns=['usernameTweet', 'text', 'datetime'])
group4 = pd.DataFrame(columns=['usernameTweet', 'text', 'datetime'])

# attack 기간에 속하는 트윗들만 담기
for i in range(len(df2017)):
    if df2017['datetime'][i] in attacks:
        group4.loc[len(group4)] = [df2017['usernameTweet'][i],df2017['text'][i],df2017['datetime'][i]]

for i in range(len(df2018)):
    if df2018['datetime'][i] in attacks:
        group4.loc[len(group4)] = [df2018['usernameTweet'][i],df2018['text'][i],df2018['datetime'][i]]

for i in range(len(df2019)):
    if df2019['datetime'][i] in attacks:
        group4.loc[len(group4)] = [df2019['usernameTweet'][i],df2019['text'][i],df2019['datetime'][i]]

#Calculating Negative, Positive, Neutral and Compound values
group1[['polarity', 'subjectivity']] = group1['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
group2[['polarity', 'subjectivity']] = group2['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
group3[['polarity', 'subjectivity']] = group3['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
group4[['polarity', 'subjectivity']] = group4['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))

for index, row in group1['text'].iteritems():
    score = SentimentIntensityAnalyzer().polarity_scores(row)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    if neg > pos:
        group1.loc[index, 'sentiment'] = 'negative'
    elif pos > neg:
        group1.loc[index, 'sentiment'] = 'positive'
    else:
        group1.loc[index, 'sentiment'] = 'neutral'
    group1.loc[index, 'neg'] = neg
    group1.loc[index, 'neu'] = neu
    group1.loc[index, 'pos'] = pos
    group1.loc[index, 'compound'] = comp

gr1 = pd.concat([gr1_2017,gr1_2018,gr1_2019])
gr2 = pd.concat([gr2_2017,gr2_2018,gr2_2019])
gr3 = pd.concat([gr3_2017,gr3_2018,gr3_2019])
gr4 = pd.concat([gr4_2017,gr4_2018,gr4_2019])

gr1_neg = []
gr1_pos = []

for i in range(len(gr1)):
    if str(gr1.index[i]).split()[0] in attacks: # 공격 기간 안에 속하면
        gr1_neg.append(gr1['neg'][i])
        gr1_pos.append(gr1['pos'][i])

# graph2017 = pd.concat([graph2017,df2017],ignore_index = True)

df2017.head(10)

df2017.datetime = pd.to_datetime(df2017.datetime) # Datetime 변환
gr4_2017 = df2017.set_index('datetime') # 인덱스로
gr4_2017 = gr4_2017.groupby(['datetime']).mean() # Group By

gr4_2017 = df2017

plt.figure(figsize=(20,5))
plt.plot(gr4_2017.index,gr4_2017['neg'],label='Negative')
plt.plot(gr4_2017.index,gr4_2017['pos'],label='Positive')
#plt.plot(gr4_2017.index,gr4_2017['neu'],label='Neural')
plt.legend(fontsize=13)

plt.figure(figsize=(20,5))
plt.plot(gr4_2017.index,gr4_2017['neg'],label='Negative')
plt.plot(gr4_2017.index,gr4_2017['pos'],label='Positive')
plt.legend(fontsize=13)


plt.figure(figsize=(20,5))
plt.plot(gr1_2017.loc[mask1].index,gr1_2017.loc[mask1]['neg'],label='Group1')
plt.plot(gr1_2017.loc[mask1].index,gr2_2017.loc[mask2]['neg'],label='Group2')
plt.plot(gr1_2017.loc[mask1].index,gr4_2017.loc[mask4]['neg'],label='Group3')
plt.plot(gr1_2017.loc[mask1].index,gr3_2017.loc[mask3]['neg'],label='Group4')
plt.title("Negative Score")
plt.legend(fontsize=13)

plt.figure(figsize=(20,5))
plt.plot(gr1_2017.loc[mask1].index,gr1_2017.loc[mask1]['pos'],label='Group1')
plt.plot(gr1_2017.loc[mask1].index,gr2_2017.loc[mask2]['pos'],label='Group2')
plt.plot(gr1_2017.loc[mask1].index,gr3_2017.loc[mask3]['pos'],label='Group3')
plt.plot(gr1_2017.loc[mask1].index,gr4_2017.loc[mask4]['pos'],label='Group4')
plt.title("Positive Score")
plt.legend(fontsize=13)

plt.figure(figsize=(20,5))
plt.plot(gr1_2017.loc[mask1].index,gr1_2017.loc[mask1]['rake_score'],label='Group1')
plt.plot(gr1_2017.loc[mask1].index,gr2_2017.loc[mask2]['rake_score'],label='Group2')
plt.plot(gr1_2017.loc[mask1].index,gr3_2017.loc[mask3]['rake_score'],label='Group3')
plt.plot(gr1_2017.loc[mask1].index,gr4_2017.loc[mask4]['rake_score'],label='Group4')
plt.title("Rake Score")
plt.legend(fontsize=13)


mask1 = (gr1_2018.index > '2018-09-01') & (gr1_2018.index <= '2018-09-30')
mask2 = (gr2_2018.index > '2018-09-01') & (gr2_2018.index <= '2018-09-30')
mask3 = (gr3_2018.index > '2018-09-01') & (gr3_2018.index <= '2018-09-30')
mask4 = (gr4_2018.index > '2018-09-01') & (gr4_2018.index <= '2018-09-30')


concat_gr1.to_csv('/Users/jungh/Downloads/PredictCyberAttacks/Group3sentimentResult.csv',sep=',', na_rep='NaN')

#Count_values for sentiment
count_values_in_column(group4,'sentiment')

# create data for Pie Chart
pichart = count_values_in_column(concat_gr1,'sentiment')
names= pichart.index
size=pichart['Percentage']
 
# Create a circle for the center of the plot
my_circle=plt.Circle( (0,0), 0.7, color='white')
plt.pie(size, labels=names, colors=['green','blue','red'])
p=plt.gcf()
p.gca().add_artist(my_circle)
plt.show()

# 추가

concat_gr1['neg'].mean()
concat_gr1['pos'].mean()
concat_gr1['neu'].mean()