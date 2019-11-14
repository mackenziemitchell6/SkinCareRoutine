#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 22:35:54 2019

@author: mackenziemitchell
"""

import nltk
from nltk.corpus import stopwords
import pandas as pd
import pickle
import numpy as np
from nltk import word_tokenize, FreqDist
import string
from os import path
from PIL import Image
import matplotlib.pyplot as plt
# from wordcloud import WordCloud, STOPWORDS,ImageColorGenerator
# from nltk.sentiment.sentiment_analyzer import SentimentAnalyzer as sa
# from nltk.classify.scikitlearn import SklearnClassifier
# from nltk.classify import ClassifierI
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy
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
from RecFunctions import skin_rec


with open('pickles/df1.pickle', 'rb') as f:
    rec = pickle.load(f)

rec=rec[~rec.prodName.str.contains('mini')]

#Creating surprise data object
data = Dataset.load_from_df(rec[['user','url','rating']],reader)
dataset = data.build_full_trainset()
print('Number of users: ',dataset.n_users,'\n') #1378
print('Number of items: ',dataset.n_items) #514

#Trying to Minimize RMSE
#SVD Grid Search
params = {'n_factors' :[10,20,30,40,50,60,70,80,90,100,200],'reg_all':[0.02,0.05,0.1,0.4,0.5,0.6],'n_epochs': [5, 10],'lr_all': [0.002, 0.005],'reg_all': [0.4, 0.6]}
g_s_svd = GridSearchCV(SVD,param_grid=params,n_jobs=-1)
g_s_svd.fit(data)
print(g_s_svd.best_score['rmse'])
print(g_s_svd.best_params['rmse'])
#0.9598922333672055
#{'n_factors': 30, 'reg_all': 0.4, 'n_epochs': 10, 'lr_all': 0.005}

#NMF Grid Search
params = {'n_factors' :[5,10,20,30,40,50,60,70,80,90,100,200],
          'n_epochs': [5, 10]}
g_s_nmf = GridSearchCV(NMF,param_grid=params,n_jobs=-1)
g_s_nmf.fit(data)
print(g_s_nmf.best_score['rmse'])
print(g_s_nmf.best_params['rmse'])
#0.992410211663158
#{'n_factors': 200, 'n_epochs': 10}

### KNN ###
#SIM_OPTIONS: Cosine Item Based
#KNN Basic
knn_basic = KNNBasic(sim_options={'name':'cosine','user_based':False})
cv_knn_basic= cross_validate(knn_basic,data,n_jobs=-1)
for i in cv_knn_basic.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_basic['test_rmse']))
# RMSE: 0.97644

#KNN Baseline
knn_baseline = KNNBaseline(sim_options={'name':'cosine','user_based':False})
cv_knn_baseline = cross_validate(knn_baseline,data)
for i in cv_knn_baseline.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_baseline['test_rmse']))
#RMSE: 0.96986

#KNN With Means
knn_means = KNNWithMeans(sim_options={'name':'cosine','user_based':False})
cv_knn_means = cross_validate(knn_means,data)
for i in cv_knn_means.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_means['test_rmse']))
#RMSE: 1.003

#SIM_OPTIONS: Cosine User Based
#KNN Basic
knn_basic = KNNBasic(sim_options={'name':'cosine','user_based':True})
cv_knn_basic= cross_validate(knn_basic,data,n_jobs=-1)
for i in cv_knn_basic.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_basic['test_rmse']))
#RMSE: 0.9785

#KNN Baseline
knn_baseline = KNNBaseline(sim_options={'name':'cosine','user_based':True})
cv_knn_baseline = cross_validate(knn_baseline,data)
for i in cv_knn_baseline.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_baseline['test_rmse']))
#RMSE: 0.9709

#KNN With Means
knn_means = KNNWithMeans(sim_options={'name':'cosine','user_based':True})
cv_knn_means = cross_validate(knn_means,data)
for i in cv_knn_means.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_means['test_rmse']))
#RMSE: 1.0308

#SIM_OPTIONS Peasrson Item Based
#KNN Basic
knn_basic = KNNBasic(sim_options={'name':'pearson','user_based':False})
cv_knn_basic= cross_validate(knn_basic,data,n_jobs=-1)
for i in cv_knn_basic.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_basic['test_rmse']))
#RMSE: 0.9732

#KNN Baseline
knn_baseline = KNNBaseline(sim_options={'name':'pearson','user_based':False})
cv_knn_baseline = cross_validate(knn_baseline,data)
for i in cv_knn_baseline.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_baseline['test_rmse']))
#RMSE: 0.9634

#KNN With Means
knn_means = KNNWithMeans(sim_options={'name':'pearson','user_based':False})
cv_knn_means = cross_validate(knn_means,data)
for i in cv_knn_means.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_means['test_rmse']))
#RMSE: 0.9923

#SIM_OPTIONS Pearson User Based
#KNN Basic
knn_basic = KNNBasic(sim_options={'name':'pearson','user_based':True})
cv_knn_basic= cross_validate(knn_basic,data,n_jobs=-1)
for i in cv_knn_basic.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_basic['test_rmse']))
#RMSE: 0.9783

#KNN Baseline
knn_baseline = KNNBaseline(sim_options={'name':'pearson','user_based':True})
cv_knn_baseline = cross_validate(knn_baseline,data)
for i in cv_knn_baseline.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_baseline['test_rmse']))
#RMSE: 0.9639

#KNN With Means
knn_means = KNNWithMeans(sim_options={'name':'pearson','user_based':True})
cv_knn_means = cross_validate(knn_means,data)
for i in cv_knn_means.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_means['test_rmse']))
#RMSE: 1.028

#SIM_OPTIONS MSD Item Based
#KNN Basic
knn_basic = KNNBasic(sim_options={'name':'msd','user_based':False})
cv_knn_basic= cross_validate(knn_basic,data,n_jobs=-1)
for i in cv_knn_basic.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_basic['test_rmse']))
#RMSE: 0.97749

#KNN Baseline
knn_baseline = KNNBaseline(sim_options={'name':'msd','user_based':False})
cv_knn_baseline = cross_validate(knn_baseline,data)
for i in cv_knn_baseline.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_baseline['test_rmse']))
#RMSE: 0.9669

#KNN With MEans
knn_means = KNNWithMeans(sim_options={'name':'msd','user_based':False})
cv_knn_means = cross_validate(knn_means,data)
for i in cv_knn_means.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_means['test_rmse']))
#RMSE: 0.9958

#SIM_OPTIONS MSD USER BASED
#KNN Basic
knn_basic = KNNBasic(sim_options={'name':'msd','user_based':True})
cv_knn_basic= cross_validate(knn_basic,data,n_jobs=-1)
for i in cv_knn_basic.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_basic['test_rmse']))
#RMSE: 0.9756

#KNN Baseline
knn_baseline = KNNBaseline(sim_options={'name':'msd','user_based':True})
cv_knn_baseline = cross_validate(knn_baseline,data)
for i in cv_knn_baseline.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_baseline['test_rmse']))
#RMSE: 0.9637

#KNN With Means
knn_means = KNNWithMeans(sim_options={'name':'msd','user_based':True})
cv_knn_means = cross_validate(knn_means,data)
for i in cv_knn_means.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_means['test_rmse']))
#RMSE: 1.022

#SIM_OPTIONS Pearson Baseline Item Based
#KNN Basic
knn_basic = KNNBasic(sim_options={'name':'pearson_baseline','user_based':False})
cv_knn_basic= cross_validate(knn_basic,data,n_jobs=-1)
for i in cv_knn_basic.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_basic['test_rmse']))
#RMSE: 0.9783

#KNN Baseline
knn_baseline = KNNBaseline(sim_options={'name':'pearson_baseline','user_based':False})
cv_knn_baseline = cross_validate(knn_baseline,data)
for i in cv_knn_baseline.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_baseline['test_rmse']))
#RMSE: 0.9645

#KNN With Means
knn_means = KNNWithMeans(sim_options={'name':'pearson_baseline','user_based':False})
cv_knn_means = cross_validate(knn_means,data)
for i in cv_knn_means.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_means['test_rmse']))
#RMSE: 0.9958

#SIM_OPTIONS Pearson Baseline User Based
#KNN Basic
knn_basic = KNNBasic(sim_options={'name':'pearson_baseline','user_based':True})
cv_knn_basic= cross_validate(knn_basic,data,n_jobs=-1)
for i in cv_knn_basic.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_basic['test_rmse']))
#RMSE: 0.9790

#KNN Baseline
knn_baseline = KNNBaseline(sim_options={'name':'pearson_baseline','user_based':True})
cv_knn_baseline = cross_validate(knn_baseline,data)
for i in cv_knn_baseline.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_baseline['test_rmse']))
#RMSE: 0.9639

#KNN With Means
knn_means = KNNWithMeans(sim_options={'name':'pearson_baseline','user_based':True})
cv_knn_means = cross_validate(knn_means,data)
for i in cv_knn_means.items():
    print(i)
print('-----------------------')
print(np.mean(cv_knn_means['test_rmse']))
#RMSE: 1.015

#Best fit model was KNN Baseline with Pearson Baseline metric and Item Based Filtering with 0.9645 RMSE
#Ready to make recommendations in python or a jupyter notebook, just call skin_rec(numProductsWanted)

