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
from surprise.model_selection import train_test_split, cross_validate, GridSearchCV 
from surprise import Dataset, Reader, accuracy, SVD, NMF
reader= Reader(rating_scale=(1, 5.0))
from surprise.prediction_algorithms import KNNBaseline
import requests
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

with open('findf.pickle', 'rb') as f:
    rec = pickle.load(f)




class Predict():
    def __init__(self):
        with open('findf.pickle', 'rb') as f:
            self.rec = pickle.load(f)
        self.model=KNNBaseline(sim_options={'name':'pearson_baseline','user_based':False})
    def get_df(self,prefs):
        mask=rec.normal==1
        col=['prodName','image','url']
        self.df=rec.loc[mask,col]
        for s in prefs:
            mask=rec.s==1
            col=['prodName','image','url']
            self.df.append(mask,col)
        self.df.drop_duplicates(inplace=True)
        #train,test=train_test_split(new_data, test_size=0.2, random_state=42, shuffle=True)
        #self.mod=self.model.fit(train)
        #return self.df,self.mod
    def ratings(self,df,num=3):
        self.to_rate=[]
        while num > 0:
            p = pd.DataFrame(self.df.sample(1))
            #brand=p[['brandName']]
            #prod=p[['prodName']]
            #url=p[['url']]
            #im=p[['image']]
            self.to_rate.append(p)
            num-=1
            
        return self.to_rate
    def new_df(self,new_ratings,raw_uid):
        self.recommend=self.df['user','url','rating']
        for n in new_ratings:
            self.recommend.append({'user':self.to_rate[0],'url':self.to_rate['url'],'rating':n})
        return self.recommend
   # def reccomend(self,new_ratings,num=5):
        
    
    
    
       # print(p[['brandName','prodName','url']])
        #rating = input('How do you rate this product on a scale of 1-5, press n if you have not used :\n')
        #if rating == 'n':
         #   continue
        #Keeping Track of the new user's ratings
     #   else:
      #      rating_one_movie = {'user':raw_uid,'url':p['url'].values[0],'rating':rating}
       #     rating_list.append(rating_one_movie) 
        #    num -= 1
   # new_ratings_df = df[['user','url','rating']].append(rating_list,ignore_index=True)
    #new_data = Dataset.load_from_df(new_ratings_df,reader)
 #   knn_baseline = KNNBaseline(sim_options={'name':'pearson_baseline','user_based':False})
  #  train, test=train_test_split(new_data, test_size=0.2, random_state=42, shuffle=True)
   # knn_baseline.fit(train)
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    