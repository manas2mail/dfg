# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 23:02:39 2017

@author: 703106491
https://www.ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
https://dev.to/rodolfoferro/sentiment-analysis-on-trumpss-tweets-using-python-

"""
# For plotting and visualization:
from IPython.display import display
from textblob import TextBlob
#from credentials import *    # This will allow us to use the keys as variables
from module.credentials import *

import pandas as pd
import numpy as np           # For number computing
import tweepy
#import csv
import re



from datetime import date, timedelta
days_before = (date.today()-timedelta(days=70)).isoformat()

# API's setup:
def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
#    api = tweepy.API(auth)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)    
    return api


def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing 
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1
    
 
    
# API's Search:
def twitter_Search(file,stCrit):
    # We create an extractor object:
    extractor = twitter_setup()
    
    A=[]
    B=[]
    C=[]
    D=[]
    E=[]
    F=[]
    G=[]
    H=[]
    I=[]
        
    #,geocode='39.8,-95.583068847656,2500km'
    for tweet in tweepy.Cursor(extractor.search,q=stCrit,count=100, lang="en", since=days_before).items():
#    for tweet in tweepy.Cursor(extractor.search,q="#cseries",count=100, lang="en", since="2017-12-2").items():                               
#        print (tweet.created_at,  tweet.user.location, tweet.user.location )
    
        A.append(len(tweet.text.encode('utf-8')))
        B.append(tweet.user.screen_name)
        C.append(tweet.created_at)
        D.append(tweet.source)   
        E.append(tweet.favorite_count)
        F.append(tweet.retweet_count)
        G.append(analize_sentiment(tweet.text))
        H.append(tweet.text.encode('utf-8'))
        I.append(tweet.user.location)  

    pd.options.html.border=0
    df=pd.DataFrame(A,columns=['len'])
    df['ID']=B
    df['Date']=C   
    df['Source']=D
    df['Likes']=E
    df['RTs']=F   
    df['SA']=G 
    df['Text']=H  
    df['location']=I      
    df['Date'] = df['Date'].dt.date  
    
#    file=r"D:\dfg\dfg\module\data\final.csv"
    df.to_csv(file, encoding='utf-8', index=False)  
    
   
    
#stCrit="#Bombardier"   
#twitter_Search(stCrit)    

    