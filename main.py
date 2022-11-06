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
    noSpecial = []
    
    linkRegex = r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)"
    noSpecialRegex = r"[^a-zA-Z0-9 \.\,\']"
    hexValue = r"\\[xX]{1}[abcdefABCDEF0-9]{2}"

    tweetLimpo = []
    for it in corpus:
        temp = re.sub(linkRegex, "", it)
        temp = re.sub(r"(https)", "", temp)
        temp = re.sub(hexValue, "", temp)
        if temp != "" and temp != "''":
            temp = re.sub(noSpecialRegex, "", temp)
            if temp != "":
                tweetLimpo.append(temp)
    noSpecial.append(tweetLimpo)

    return tweetLimpo

def tokenizar(text):
    tokens = []
    
    for it in text:
        temp = nltk.tokenize.word_tokenize(it)
        tokens.append(temp)

    return tokens

dataFrame = readFiles()
lista = []
texts = lowerCase(dataFrame['text'])

for it in texts:
    if "lazarus" in it:
        lista.append(it)

print(len(lista))

lista = removeSpecialChar(lista)

tokens = tokenizar(lista)


print(len(lista))
print(len(tokens))
print(lista)

nlp = spacy.load("en_core_web_sm")

f = open("test.txt", "w")

for item in lista:
    doc = nlp(item)
    v = []
    for ent in doc.ents:
        v.append([ent.text, ent.label_])
    f.write(str(v))
    f.write("\n")

f.close()

print('end')


