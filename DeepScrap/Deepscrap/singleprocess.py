import subprocess
import json

with open('/Users/jungh/Desktop/grouping/group_screen_name/group4_screen_name.json', 'r') as json_file:
    json_data = json.load(json_file)
    for i in range(10):
        user = json_data[i]['username']
    #userIDs = f.read().split(',')
    #for userID in userIDs:
        print("userID:", user)
        subprocess.call(['scrapy', 'crawl_many', '-a', user, '-o', 'output.json', '-t', 'json'])







