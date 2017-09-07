import twitter
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
from geopy.geocoders import Nominatim

geolocator = Nominatim()


CONSUMER_KEY=''
CONSUMER_SECRET=''
OAUTH_TOKEN=''
OAUTH_TOKEN_SECRET=''


auth = twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

print (twitter_api)


def twitter_mining(q,count,geocode):
    search_results = twitter_api.search.tweets(q=q,count=count, geocode=geocode)
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
        if statuses[i]['text']:
            print(str(statuses[i]['text'])) 
    return sentiment*100 

if __name__=='__main__':
    q=['jokowi']
    count = 100
    s=[]
    
    lokasi = "Jakarta"
    location = geolocator.geocode(lokasi)
    radius = 1000
    geocode = "%f,%f,%dkm" %(location.latitude,location.longitude,radius)    
        
    for i in q:
        s.append(twitter_mining(i,count,geocode))
    
    y_pos = np.arange(len(s))
    #q=['jokowi']
    if len(q)>1:
        plt.bar(y_pos, s, align='center', alpha=0.5)
        plt.xticks(y_pos, q)
        plt.title('public sentiment (%)')
    elif len(q)==1:
        print ("%.2f%% " %(s[0]))
