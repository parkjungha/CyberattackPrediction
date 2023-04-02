import tweepy   
import pandas as pd     # To handle data



def getID():
    filedir = '/Users/jungh/Desktop/RecordedFuture_ID.txt'
    str=''
    file = open(filedir,'r',encoding='utf-8')
    str = file.read()
    IDList = str.strip().split("', '")
    IDList = [i.lower() for i in IDList]
    IDList = [i.strip() for i in IDList]
    my_set =set(IDList)
    IDList= list(my_set)
    return IDList
    file.close()
    
    
# Consumer API keys:
CONSUMER_KEY = "4oqZjge7qM0n3WNftJiKHFtOF" #API key
CONSUMER_SECRET = "CZOzvRcdwFOzPZFoM5igXVGBbOBp7lQWBBtCRe76wuv738equP" 
ACCESS_TOKEN = "1004411169568747520-7NBYDlDKlGXX9q5gjXasgRRo5p3HtT" 
ACCESS_TOKEN_SECRET = "b3BSPhEfHGYCxuIaNPg1CFcJtKkCWnjIZESooDgT99GWL" 

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_delay=10)

accountlist = pd.DataFrame(getID())
accountlist['screen_name']=None
accountlist['location']=None
activated_count = 0
located_count = 0

for i in range(len(accountlist)):
    try:
        name = api.get_user(accountlist[0][i]).screen_name
        accountlist['screen_name'][i] = name
        lo = api.get_user(accountlist[0][i]).location
        accountlist['location'][i] = lo
        if lo != "":
            located_count += 1
        activated_count += 1
        print(i,name,lo)
    except:
        accountlist['screen_name'][i] = None
        
activated_list = accountlist.dropna(subset=["screen_name"])


for i in range(len(activated_list)):
    if activated_list[0][i] != activated_list['screen_name'][i].lower():
        print("ERROR")
        

activated_list = activated_list.drop(activated_list.columns[[0]], axis=1)

with open('/Users/jungh/Downloads/PredictCyberAttacks/userList_Location_.json', 'w') as f:
    f.write(activated_list.to_json(orient='records', lines=True))
