##from tweepy import *
import tweepy 
import pandas as pd
import csv
import re 
import string
import preprocessor as p
 
consumer_key = "<consumer_key>"
consumer_secret = "<consumer_secret>"
access_key= "<access_key>"
access_secret = "<access_secret>"
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
 
api = tweepy.API(auth,wait_on_rate_limit=True)
 
csvFile = open('file-name', 'w')
csvWriter = csv.writer(csvFile,delimiter=";")
 
search_words = "cyberattack OR \"zero day\" OR ramsonware" # enter your words
new_search = search_words + " -filter:retweets"
 
for tweet in tweepy.Cursor(api.search_tweets,q=new_search,count=100,lang="en",since_id=0,include_entities=True).items():
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'),tweet.user.screen_name.encode('utf-8'), tweet.user.location.encode('utf-8')])
