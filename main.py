##from tweepy import *
import tweepy 
import pandas as pd
import csv
import re 
import string
import preprocessor as p
 
consumer_key = "s29T1F9InPxHrsWruI6ALmOWO"
consumer_secret = "tc9e2CI7AboCWuek7MMfdlcLJuDeRYk7eKmBj2tXMhfVv12EoF"
access_key= "65904150-sp4Yl3RAw18RZHR4jCR8qTZx56qzp8nEWuBipJfIR"
access_secret = "KadnvQ66AgJz3xyWG5Ncfd7AguMdeY76EAQBGfTpKxpEN"
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
 
api = tweepy.API(auth,wait_on_rate_limit=True)
 
csvFile = open('file-name', 'w')
csvWriter = csv.writer(csvFile,delimiter=";")
 
search_words = "cyberattack OR \"zero day\" OR ramsonware" # enter your words
new_search = search_words + " -filter:retweets"
 
for tweet in tweepy.Cursor(api.search_tweets,q=new_search,count=100,lang="en",since_id=0,include_entities=True).items():
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'),tweet.user.screen_name.encode('utf-8'), tweet.user.location.encode('utf-8')])