#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 11:37:25 2019

@author: mackenziemitchell
"""
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import pickle
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

def get_products_by_type(product_type,maxpages):
    types=[]
    for i in range(0,maxpages):
        response=requests.get('https://www.skinstore.com/skin-care/{}.list?pageNumber={}'.format(product_type,i))
        soup=BeautifulSoup(response.content,'html.parser')
        prods=soup.findAll('h2',{'class':'productBlock_productName'})
    
        for p in prods:
            types.append(p.text.strip('\n'))
    return types

def get_products_by_problem(problem,maxpages):
    dfdict=[]
    prodlist=[]
    for i in range(0,maxpages):
        response=requests.get('https://www.skinstore.com/skin-care/skincare-concern/{}.list?pageNumber={}'.format(problem,i))
        soup=BeautifulSoup(response.content,'html.parser')
        brands=soup.findAll('h2',{'class':'productBlock_productName'})
        ratings=soup.findAll('span',{'class':'productBlock_ratingValue'})
        urls=soup.findAll('span',{'class':'js-enhanced-ecommerce-data hidden'},{'data-product-id':True})
        prices=soup.findAll('span',{'class':'productBlock_priceValue'})
#         images=soup.findAll('div',{'class':'productBlock_imageContainer'},{'src':True})
        for b,r,p,u in zip(brands,ratings,prices,urls):
            prodlist.append(b.text.strip('\n'))
            dfdict.append({'prodName':b.text.strip('\n'),'rating':r.text,'price':p.text.strip('$'),'type':['acne','blemishes'],'url':str(u).split('data-product-master-product-id=')[1][1:9]})
        #for images... for i in images:
            #'image':(str(i).split('"'))[-2]
    df=pd.DataFrame(dfdict)
    return (df,prodlist)

def categorical_columns(colname,lis,dataframe):
    category=[]
    for f in dataframe.prodName:
        if f in lis:
            category.append(1)
        else:
            category.append(0)
    dataframe[colname.replace(',','')]=category

def type_column(dataframe):
    types=['cleanser','exfoliator','makeup-removers','toner','mist','treatment','serum','lotion','moisturizer',
             'balm','oil','mask','peel','lip','eye','supplement','tool']
    typelist=[]
    for prod in dataframe.prodName:
        for t in types:
            if prod in t:
                typelist.append(t)
    return typelist

#Functions for EDA
def type_prod_histogram(df,title):
    plt.figure(figsize=(12,10))
    plt.title(title)
    dicttypes={'oil':sum(df.oil),'cleanser':sum(df.cleanser),'exfoliator':sum(df.exfoliator),'remover':sum(df['makeup-removers']),
                'toner':sum(df.toner),'mist':sum(df.mist),'treatment':sum(df.treatment),'serum':sum(df.serum),'lotion':sum(df.lotion),
                'moisturizer':sum(df.moisturizer),'balm':sum(df.balm),'mask':sum(df['mask']),'peel':sum(df['peel']),'lip':sum(df['lip']),
                'eye':sum(df['eye']),'supplment':sum(df['supplement']),'tool':sum(df['tool'])}
    sns.barplot(x=list(dicttypes.keys()),y=list(dicttypes.values()))
    plt.xticks(rotation=45)
    plt.savefig('{}TypesHistogram.png'.format(title))
    print((dicttypes))
    return(sns.barplot(x=list(dicttypes.keys()),y=list(dicttypes.values())))
def type_problem_histogram(df,title):
    plt.figure(figsize=(12,10))
    plt.title(title)
    dictprobs={'age':sum(df.age),'darkCircles':sum(df.darkcircles),'acne':sum(df.acne),'dry':sum(df.dry),
                'redness':sum(df.redness),'sensitive':sum(df.sensitive),'oily':sum(df.oily),'normal':sum(df.normal)}
    sns.barplot(x=list(dictprobs.keys()),y=list(dictprobs.values()))
    plt.xticks(rotation=45)
    plt.savefig('{}ProblemsHistogram.png'.format(title))
    print(dictprobs)
    return sns.barplot(x=list(dictprobs.keys()),y=list(dictprobs.values()))

#Functions for Recommender System
def skin_rater(movie_df,num, typ=None):
    rating_list = []
    #Start with 'normal/combination skin df'
    df=movie_df.loc[movie_df['normal']==1].copy()
    raw_uid=input('type username: ')
    #filter df by preferences
    stype=input('What is your skin type or skin problems? Type all that apply: dry, sensitive, oily, redness, dark circles, aging. (n if none apply) ')
    ptype=input('Are you looking for any of these products? \ncleanser \nexfoliator\n makeup-remover\n toner \nmist \ntreatment \nserum \n lotion \nmoisturizer \nbalm \noil \nmask \npeel \nlip \neye \nsupplement \ntool ')
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
        print(p[['brandName','prodName','url']])
        rating = input('How do you rate this movie on a scale of 1-5, press n if you have not seen :\n')
        if rating == 'n':
            continue
        #Keeping Track of the new user's ratings
        else:
            rating_one_movie = {'user':raw_uid,'url':p['url'].values[0],'rating':rating}
            rating_list.append(rating_one_movie) 
            num -= 1
    return(rating_list,raw_uid,df)

def rank_prods_for_user(df,raw_uid):
    list_of_prods=[]
    for u in df['url'].unique():
        list_of_prods.append((u,knn_baseline.predict(raw_uid,u)[3]))
    ranked_prods = sorted(list_of_prods,key=lambda x:x[1],reverse=True)
    return (ranked_prods)
def recommended_products(user_ratings,df):
    n=int(input('How many products are you looking for?\n'))
    for idx, re in enumerate(user_ratings):
        title = df.loc[df['url'] == int(re[0])]['prodName']
        u=re[0]
        print('Recommendation # ',idx+1,'|| ', 'url:', u, '||','product: ', df[df['url']==u]['prodName'].drop_duplicates(),'\n')
        n-= 1
        if n == 0:
            break
        
def skin_rec(num, movie_df=rec, typ=None):
    rating_list = []
    knn_baseline = KNNBaseline(sim_options={'name':'pearson_baseline','user_based':False})
    #Start with 'normal/combination skin df'
    df=movie_df.loc[movie_df['normal']==1].copy()
    raw_uid=input('type username: ')
    #filter df by preferences
    stype=input('What is your skin type or skin problems? Type all that apply: \ndry \nsensitive \noily \nredness \ndark circles \naging \n(n if none apply):\n ')
    ptype=input('Are you looking for any of these products? \ncleanser \nexfoliator\nmakeup-remover\ntoner \nmist \ntreatment \nserum \nlotion \nmoisturizer \nbalm \noil \nmask \npeel \nlip \neye \nsupplement \ntool:\n ')
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
    if 'cleanser' in ptype:
        df=pd.concat([df,movie_df[movie_df['cleanser']==1]])
    if 'exfoliator' in ptype:
        df=pd.concat([df,movie_df[movie_df['exfoliator']==1]])
    if 'makeup-remover' in ptype:
        df=pd.concat([df,movie_df[movie_df['makeup-removers']==1]])
    if 'toner' in ptype:
        df=pd.concat([df,movie_df[movie_df['toner']==1]])
    if 'mist' in ptype:
        df=pd.concat([df,movie_df[movie_df['mist']==1]])
    if 'treatment' in ptype:
        df=pd.concat([df,movie_df[movie_df['treatment']==1]])
    if 'serum' in ptype:
        df=pd.concat([df,movie_df[movie_df['serum']==1]])
    if 'lotion' in ptype:
        df=pd.concat([df,movie_df[movie_df['lotion']==1]])
    if 'moisturizer' in ptype:
        df=pd.concat([df,movie_df[movie_df['moisturizer']==1]])
    if 'balm' in ptype:
        df=pd.concat([df,movie_df[movie_df['balm']==1]])
    if 'oil' in ptype:
        df=pd.concat([df,movie_df[movie_df['oil']==1]])
    if 'mask' in ptype:
        df=pd.concat([df,movie_df[movie_df['mask']==1]])
    if 'peel' in ptype:
        df=pd.concat([df,movie_df[movie_df['peel']==1]])
    if 'lip' in ptype:
        df=pd.concat([df,movie_df[movie_df['lip']==1]])
    if 'eye' in ptype:
        df=pd.concat([df,movie_df[movie_df['eye']==1]])
    if 'supplement' in ptype:
        df=pd.concat([df,movie_df[movie_df['supplement']==1]])
    if 'tool' in ptype:
        df=pd.concat([df,movie_df[movie_df['tool']==1]])
    df.drop_duplicates(inplace=True)
    #Asking User to rate these products from their preferences
    while num > 0:
        p = df.sample(1)
#         response = requests.get('https://' + p['image'].item())
#         img = Image.open(BytesIO(response.content))
#         print(p[['brandName','prodName','url']],'https://' + str(p['image']))
        print(p[['prodName','url']])
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
        print('Recommendation # ',idx+1,'|| ', 'url:', u, '||','product: ', df[df['url']==u]['prodName'].drop_duplicates(),'\n')
        n-= 1
        if n == 0:
            break