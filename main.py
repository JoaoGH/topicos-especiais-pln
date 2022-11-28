import time
from datetime import datetime
import tweepy
import pandas as pd
import csv
import re
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

    filename = str(datetime.now().replace(microsecond=0).isoformat()).replace(':', '-')
    csvFile = open('./corpus/' + filename, 'w')
    csvWriter = csv.writer(csvFile,delimiter=";")

    search_words = ""
    print("1 - Informar argumentos para a busca")
    print("2 - Realizar busca com base no dicionario")
    opc = int(input())
    if (opc == 1):
        palavras = input("\tEntre com uma lista de argumentos para busca separados por ','")
        search_words = palavras.split(",")
    else:
        f = open("attacks_dictionary.txt", 'r')
        search_words = []
        for line in f:
            search_words.append(line.strip().lower())

    print("Realizando busca dos tweets...")
    for it in search_words:
        new_search = it + " -filter:retweets"
        max = 0
        for tweet in tweepy.Cursor(api.search_tweets, q=new_search, count=400, lang="en", since_id=0, include_entities=True).items():
            max = max + 1
            if (max == 500):
                break
            csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'), tweet.user.screen_name.encode('utf-8'), tweet.user.location.encode('utf-8')])
    print("Busca finalizada com sucesso.")

def readFiles():
    nomeArquivos = os.listdir("./corpus/")

    fileName = "./corpus/all.csv"

    if os.path.isfile(fileName):
        os.remove(fileName)

    fileAllTweets = open(fileName, "a")
    fileAllTweets.write("id;date;text;user;location\n")

    i = 0
    for it in nomeArquivos:
        if (it == "all.csv"):
            continue
        with open("./corpus/" + it, "r") as reader:
            for line in reader:
                if line.strip():
                    i = i + 1
                    fileAllTweets.write(str(i) + ";" + line)
            fileAllTweets.truncate()
    fileAllTweets.close()

    df = pd.read_csv(fileName, delimiter=';', encoding="ansi")
    df.columns = ['id', 'date', 'text', 'user', 'location']

    return df

def lowerCase(corpus):
    corpus["text"] = corpus["text"].str.lower()
    
    return corpus

def removeSpecialChar(corpus):
    linkRegex = r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)"
    noSpecialRegex = r"[^a-zA-Z0-9 \.\,\']"
    hexValue = r"\\[xX]{1}[abcdefABCDEF0-9]{2}"
    byteRegex = r"^(['\"]?b['\"])"

    corpus["text"] = corpus["text"].map(lambda x: re.sub(byteRegex, '', x))
    corpus["text"] = corpus["text"].map(lambda x: re.sub(hexValue, '', x))
    corpus["text"] = corpus["text"].map(lambda x: re.sub(linkRegex, '', x))
    corpus["text"] = corpus["text"].map(lambda x: re.sub(noSpecialRegex, '', x))

    return corpus

def textCleaning(corpus):
    dictionary = []

    f = open('groups_dictionary.txt', 'r')
    for line in f:
        dictionary.append(line.strip().lower())
    f.close()

    corpus = corpus[corpus["text"].str.contains("|".join(dictionary), case=False)]

    return corpus

def doIdentifications(corpus):
    fileName = "identification.txt"

    nlp = spacy.load("en_core_web_sm")
    identify(corpus, nlp, fileName)

    fileName = "identification-2.txt"

    nlp = spacy.load("./model-best/")
    identify(corpus, nlp, fileName)

def identify(corpus, nlp, fileName):
    f = open(fileName, "w")

    for i in range(0, len(corpus)):
        doc = nlp(corpus.iloc[i].text)
        id = corpus.iloc[i].id
        v = []
        for ent in doc.ents:
            v.append([ent.text, ent.label_])
        if v:
            f.write(str(id) + ";" + str(v))
            f.write("\n")

    f.close()

def pipeline():
    print("Executando pipeline...")

    dataFrame = readFiles()

    dataFrame = lowerCase(dataFrame)
    dataFrame = textCleaning(dataFrame)
    dataFrame = removeSpecialChar(dataFrame)

    doIdentifications(dataFrame)

    print("Pipeline executado com sucesso.")
    print()
    return dataFrame

dataFrame = None
opc = 0
while opc != 4:
    print()
    print("--------- Topicos Especiais - NLP ---------")
    print("1 - Buscar tweets")
    print("2 - Executar pipeline")
    print("3 - Analisar dados")
    print("4 - Sair")
    opc = int(input())
    print()

    if opc == 1:
        findTweet()
    elif opc == 2:
        dataFrame = pipeline()
    elif opc == 3:
        print("exibir graficos")
        time.sleep(2)





