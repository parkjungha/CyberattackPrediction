import json

for j in range(1,5): 
    json_data = open('/Users/jungh/Desktop/grouping/group_profile/group'+str(j)+'_profile.json',encoding="utf-8").read()
    data = json.loads(json_data)

    num_follower = [] #follower 수
    num_following = [] #following 수
    num_rate = [] #following/follower 비율
    securityResearchers = 0
    blank = 0

    for i in range(len(data)): 
        num_follower.append(data[i]['followers_count'])
        num_following.append(data[i]['friends_count'])
        if "security research" in data[i]['description'].lower():
            securityResearchers += 1
        if (data[i]['description'] == ""):
            blank +=1

    print(num_rate)
    print("The number of people in Group"+str(j)+" is ",len(data))
    print(len(num_follower)==len(num_following)==len(num_rate))
    print("Group"+str(j)+": The average number of followers is ",sum(num_follower, 0.0)/len(num_follower))
    print("Group"+str(j)+": The average number of following is ",sum(num_following, 0.0)/len(num_following))
    print("Group"+str(j)+": The average rate of following/follower is ",(sum(num_following, 0.0)/len(num_following))/(sum(num_follower, 0.0)/len(num_follower)))
    print("Group"+str(j)+": The number of security researchers inferred by the description is ",securityResearchers)
    print("Group"+str(j)+": The number of people whose description is blank ",blank)
    print()