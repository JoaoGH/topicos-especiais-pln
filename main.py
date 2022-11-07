##from tweepy import *
import tweepy 
import pandas as pd
import csv
import re 
import string
import preprocessor as p
import nltk
import spacy
import os

def findTweet():
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

def readFiles():

    nomeArquivos = os.listdir("./corpus/")

    fileName = "./corpus/all.csv"

    if os.path.isfile(fileName):
        os.remove(fileName)

    f2 = open(fileName, "a")
    f2.write("date;text;user;location\n\n")

    for it in nomeArquivos:
        f1 = open("./corpus/" + it, "r")
        f2.write(f1.read())
        f1.close()
    f2.close()

    df = pd.read_csv(fileName, delimiter=';', encoding="ansi")
    df.columns = ['date', 'text', 'user', 'location']

    return df

def lowerCase(corpus):
    corpus["text"] = corpus["text"].str.lower()
    
    return corpus

def removeSpecialChar(corpus):
    linkRegex = r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)"
    noSpecialRegex = r"[^a-zA-Z0-9 \.\,\']"
    hexValue = r"\\[xX]{1}[abcdefABCDEF0-9]{2}"

    corpus["text"] = corpus["text"].map(lambda x: re.sub(linkRegex, '', x))
    corpus["text"] = corpus["text"].map(lambda x: re.sub(noSpecialRegex, '', x))
    corpus["text"] = corpus["text"].map(lambda x: re.sub(hexValue, '', x))

    return corpus

def textCleaning(corpus):
    dictionary = ["lazarus"]

    corpus = corpus[corpus["text"].str.contains("|".join(dictionary), case=False)]

    return corpus

dataFrame = readFiles()
print(len(dataFrame))

dataFrame = lowerCase(dataFrame)
dataFrame = textCleaning(dataFrame)
dataFrame = removeSpecialChar(dataFrame)

print(len(dataFrame))

print('end')


