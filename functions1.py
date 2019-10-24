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

#with open('userratingsDF.pickle', 'rb') as f:
 #   dfr = pickle.load(f)
with open('CategoricalItemDF.pickle', 'rb') as f:
    full = pickle.load(f)
#with open('_SENT&RATINGDF.pickle', 'rb') as f:
 #   df1 = pickle.load(f)
with open('recdf.pickle', 'rb') as f:
    rec1 = pickle.load(f)
with open('findf.pickle', 'rb') as f:
    rec = pickle.load(f)
with open('ratingsmeandf.pickle', 'rb') as f:
    ratemean = pickle.load(f)
#with open('newratingsDFwithimg.pickle', 'rb') as f:
 #   images = pickle.load(f)
df=rec[rec['normal']==1]
 
def get_dataframe(stype):
    df=rec[rec['normal']==1]
    for s in stype:
        df=df.append(rec[rec[s]==1])
    df.drop_duplicates(inplace=True)
    return df

def get_samples(df,num=3):
    torate=[]
    while num>0:
        p=df.sample(1)
        torate.append(p[['prodName','url']])
    return torate


def skin_rater(new_rates):
    knn_baseline = KNNBaseline(sim_options={'name':'pearson_baseline','user_based':False})
    new_ratings_df = df[['user','url','rating']].append(new_rates,ignore_index=True)
    new_data = Dataset.load_from_df(new_ratings_df,reader)
    train, test=train_test_split(new_data, test_size=0.2, random_state=42, shuffle=True)
    knn_baseline.fit(train)
    #preds=knn_baseline.test(test)
    
    list_of_prods=[]
    for u in new_ratings_df['url'].unique():
        list_of_prods.append((u,knn_baseline.predict(raw_uid,u)[3]))
    ranked_prods = sorted(list_of_prods,key=lambda x:x[1],reverse=True)
    
    return ranked_prods[2:]

#def skin_rater(movie_df,num, raw_uid):
    #rating_list = []
#    knn_baseline = KNNBaseline(sim_options={'name':'pearson_baseline','user_based':False})
  #  while num > 0:
   #     p = df.sample(1)
#         response = requests.get('https://' + p['image'].item())
#         img = Image.open(BytesIO(response.content))
#         print(p[['brandName','prodName','url']],'https://' + str(p['image']))
    #    print(p[['brandName','prodName','url']])
     #   rating = input('How do you rate this product on a scale of 1-5, press n if you have not used :\n')
      #  if rating == 'n':
       #     continue
        #Keeping Track of the new user's ratings
        #else:
         #   rating_one_movie = {'user':raw_uid,'url':p['url'].values[0],'rating':rating}
          #  rating_list.append(rating_one_movie) 
           # num -= 1
#    new_ratings_df = df[['user','url','rating']].append(rating_list,ignore_index=True)
 #   new_data = Dataset.load_from_df(new_ratings_df,reader)
  #  train, test=train_test_split(new_data, test_size=0.2, random_state=42, shuffle=True)
   # knn_baseline.fit(train)
    #preds=knn_baseline.test(test)
    
  #  list_of_prods=[]
   # for u in new_ratings_df['url'].unique():
    #    list_of_prods.append((u,knn_baseline.predict(raw_uid,u)[3]))
    r#anked_prods = sorted(list_of_prods,key=lambda x:x[1],reverse=True)
    
  #  return ranked_prods[2:]
    