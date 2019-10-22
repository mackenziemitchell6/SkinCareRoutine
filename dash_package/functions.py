#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 13:34:28 2019

@author: mackenziemitchell
"""
import pandas as pd
import pickle
import numpy as np
import string
from os import path
from PIL import Image
import matplotlib.pyplot as plt
# from wordcloud import WordCloud, STOPWORDS,ImageColorGenerator
# from nltk.sentiment.sentiment_analyzer import SentimentAnalyzer as sa
# from nltk.classify.scikitlearn import SklearnClassifier
# from nltk.classify import ClassifierI
from surprise.prediction_algorithms import knns
from surprise.similarities import cosine, msd, pearson
from surprise.model_selection import train_test_split, cross_validate
from surprise import Dataset, Reader, accuracy, SVD, NMF
reader= Reader(rating_scale=(1, 5.0))
from surprise.prediction_algorithms import KNNWithMeans, KNNBasic, KNNBaseline
from surprise.model_selection import cross_validate, GridSearchCV
from surprise import Trainset
import requests
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

with open('userratingsDF.pickle', 'rb') as f:
    dfr = pickle.load(f)
with open('CategoricalItemDF.pickle', 'rb') as f:
    full = pickle.load(f)
with open('_SENT&RATINGDF.pickle', 'rb') as f:
    df1 = pickle.load(f)
with open('recdf.pickle', 'rb') as f:
    rec = pickle.load(f)
with open('ratingsmeandf.pickle', 'rb') as f:
    ratemean = pickle.load(f)
with open('newratingsDFwithimg.pickle', 'rb') as f:
    images = pickle.load(f)

def skin_rater(movie_df,num, stype=None,ptype=None):
    rating_list = []
    knn_baseline = KNNBaseline(sim_options={'name':'pearson_baseline','user_based':False})
    #Start with 'normal/combination skin df'
    df=movie_df.loc[movie_df['normal']==1].copy()
    raw_uid=input('type username: ')
    #filter df by preferences
    #stype=input('What is your skin type or skin problems? Type all that apply: dry, sensitive, oily, redness, dark circles, aging. (n if none apply) ')
    #ptype=input('Are you looking for any of these products? \ncleanser \nexfoliator\n makeup-remover\n toner \nmist \ntreatment \nserum \n lotion \nmoisturizer \nbalm \noil \nmask \npeel \nlip \neye \nsupplement \ntool ')
    if 'dry' in stype:
        df=pd.concat([df,movie_df[movie_df['dry']==1]])
    if 'aging' in stype:
        df=pd.concat([df,movie_df[movie_df['age']==1]])
    if 'dark circles' in stype:
        df=pd.concat([df,movie_df[movie_df['darkcircles']==1]])
    if 'redness' in stype:
        df=pd.concat([df,movie_df[movie_df['redness']==1]])
    if 'sensitive' in stype:
        df=pd.concat([df,movie_df[movie_df['sensitive']==1]])
    if 'oily' in stype:
        df=pd.concat([df,movie_df[movie_df['oily']==1]])
    if 'cleanser' in stype:
        df=pd.concat([df,movie_df[movie_df['cleanser']==1]])
    if 'exfoliator' in stype:
        df=pd.concat([df,movie_df[movie_df['exfoliator']==1]])
    if 'makeup-remover' in stype:
        df=pd.concat([df,movie_df[movie_df['makeup-removers']==1]])
    if 'toner' in stype:
        df=pd.concat([df,movie_df[movie_df['toner']==1]])
    if 'mist' in stype:
        df=pd.concat([df,movie_df[movie_df['mist']==1]])
    if 'treatment' in stype:
        df=pd.concat([df,movie_df[movie_df['treatment']==1]])
    if 'serum' in stype:
        df=pd.concat([df,movie_df[movie_df['serum']==1]])
    if 'lotion' in stype:
        df=pd.concat([df,movie_df[movie_df['lotion']==1]])
    if 'moisturizer' in stype:
        df=pd.concat([df,movie_df[movie_df['moisturizer']==1]])
    if 'balm' in stype:
        df=pd.concat([df,movie_df[movie_df['balm']==1]])
    if 'oil' in stype:
        df=pd.concat([df,movie_df[movie_df['oil']==1]])
    if 'mask' in stype:
        df=pd.concat([df,movie_df[movie_df['mask']==1]])
    if 'peel' in stype:
        df=pd.concat([df,movie_df[movie_df['peel']==1]])
    if 'lip' in stype:
        df=pd.concat([df,movie_df[movie_df['lip']==1]])
    if 'eye' in stype:
        df=pd.concat([df,movie_df[movie_df['eye']==1]])
    if 'supplement' in stype:
        df=pd.concat([df,movie_df[movie_df['supplement']==1]])
    if 'tool' in stype:
        df=pd.concat([df,movie_df[movie_df['tool']==1]])
    df.drop_duplicates(inplace=True)
    #Asking User to rate these products from their preferences
    while num > 0:
        p = df.sample(1)
#         response = requests.get('https://' + p['image'].item())
#         img = Image.open(BytesIO(response.content))
#         print(p[['brandName','prodName','url']],'https://' + str(p['image']))
        print(p[['brandName','prodName','url']])
        rating = input('How do you rate this product on a scale of 1-5, press n if you have not used :\n')
        if rating == 'n':
            continue
        #Keeping Track of the new user's ratings
        else:
            rating_one_movie = {'user':raw_uid,'url':p['url'].values[0],'rating':rating}
            rating_list.append(rating_one_movie) 
            num -= 1
    new_ratings_df = df[['user','url','rating']].append(rating_list,ignore_index=True)
    new_data = Dataset.load_from_df(new_ratings_df,reader)
    train, test=train_test_split(new_data, test_size=0.2, random_state=42, shuffle=True)
    knn_baseline.fit(train)
    #preds=knn_baseline.test(test)
    
    list_of_prods=[]
    for u in new_ratings_df['url'].unique():
        list_of_prods.append((u,knn_baseline.predict(raw_uid,u)[3]))
    ranked_prods = sorted(list_of_prods,key=lambda x:x[1],reverse=True)
    
    n=int(input('How many products are you looking for?\n'))
    for idx, re in enumerate(ranked_prods[2:]):
        title = df.loc[df['url'] == int(re[0])]['prodName']
        u=re[0]
        print('Recommendation # ',idx+1,'|| ', 'url:', u, 'image: ', '||','product: ', df[df['url']==u]['prodName'].drop_duplicates(),'\n')
        n-= 1
        if n == 0:
            break
    