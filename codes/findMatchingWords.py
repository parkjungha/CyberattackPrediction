import json
import os
import pandas as pd
from collections import Counter

def getKeyword():
    filedir = '/Users/jungh/Desktop/industry_term.txt'
    str=''
    file = open(filedir,'r',encoding='utf-8')
    str = file.read()
    keywordList = str.strip().split("', '")
    keywordList = [i.lower() for i in keywordList]
    my_set =set(keywordList)
    keywordList= list(my_set)
    return keywordList
    file.close()

keywordList = getKeyword()

# jdata = open("/Users/jungh/Desktop/getTweetText/gr1_processed/admdeJong.json", encoding="utf-8").read()
# data = json.loads(jdata)
# text =''
# for j in range(len(data)):
#         text = text+" "+data[j]['text']
  
# matchingWord = [] 
# for item in keywordList:
#       if item in text:
#             matchingWord.append(item)
            
files = os.listdir('/Users/jungh/Desktop/getTweetText/gr2_processed')
df = []
allWordList = []
for i in range(len(files)):
    jdata = open("/Users/jungh/Desktop/getTweetText/gr2_processed/"+str(files[i]), encoding="utf-8").read()
    data = json.loads(jdata)
    size = len(data)
    if (data == []):
        continue
    text =''
    for j in range(len(data)):
        text = text+" "+data[j]['text']

    matchingWord = [] 
    for item in keywordList:
          if item in text:
                matchingWord.append(item)
    allWordList += matchingWord
    df.append([str(files[i]).split('.')[0],len(matchingWord), size])

df = pd.DataFrame(df,columns=['username','num of matchings','size'])
df.sort_values(by='num of matchings',ascending=False, inplace=True)
df.to_csv("/Users/jungh/Desktop/getTweetText/simpleMatching_gr2.csv", sep=',', na_rep='NaN')

di = dict(Counter(allWordList))

sortedDict = dict(sorted(di.items(), key=lambda t : t[1], reverse=True))

with open("/Users/jungh/Desktop/getTweetText/countWord_gr2.json", "w") as json_file:
    json.dump(sortedDict,json_file)