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

    date = df['date']
    text = df['text']
    user = df['user']

    return df

def lowerCase(corpus):
    lowers = []
    
    for it in corpus:
        lowers.append(it.lower())
    
    return lowers

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


