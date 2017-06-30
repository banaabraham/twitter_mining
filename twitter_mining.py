# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 17:00:13 2017

@author: lenovo
"""

import twitter
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np

CONSUMER_KEY=''
CONSUMER_SECRET=''
OAUTH_TOKEN=''
OAUTH_TOKEN_SECRET=''


auth = twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

print (twitter_api)
WORLD_WOE_ID = 1
USE_WOE_id = 2
#world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)

#print (json.dumps(world_trends, indent=1))

q=['oppo','nokia','xiomi','LG phone','Samsung Phone']
count = 100
def twitter_mining(q,count):
    search_results=twitter_api.search.tweets(q=q,count=count)
    statuses = search_results['statuses']

    for _ in range(3):
        print ("lenght of statuses %d" %(len(statuses)))
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError:
                break
        kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])
        search_results = twitter_api.search.tweets(**kwargs)
        statuses+= search_results['statuses']
    positive=0  
    null=0  
    for i in range(len(statuses)):
        blob = TextBlob(str(statuses[i]['text'])).sentiment
        if blob.subjectivity == 0:
            null+=1
        if blob.polarity>0:
            positive+=1           
            sentiment=positive/(len(statuses))
    return sentiment*100 
s=[]   
for i in q:
    s.append(twitter_mining(i,count))
    
y_pos = np.arange(len(s))
q=['oppo','nokia','xiomi','LG','Samsung']
plt.bar(y_pos, s, align='center', alpha=0.5)
plt.xticks(y_pos, q)
plt.title('market sentiment (%)')   
    
