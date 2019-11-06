#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 12:33:27 2019

@author: mackenziemitchell
"""

import streamlit as st
import pandas as pd
import pickle
from surprise.prediction_algorithms import KNNBaseline
from surprise import Dataset, Reader
reader= Reader(rating_scale=(1, 5.0))
from surprise.model_selection import train_test_split

st.title("Skincare Routine Recommender")
from PIL import Image
st.image(Image.open("dash_package/static/washing-face.jpg"),width=800)

st.header("Find the Perfect Skincare Routine for your Skin Type!")

with open('pickles/df1.pickle', 'rb') as f:
    rec = pickle.load(f)
df=rec.loc[rec['normal']==1].copy()

def user():
    raw_uid=st.text_input("Please Enter a Username:")
    return raw_uid
def get_df(df,movie_df):
    #rating_list = []
    #knn_baseline = KNNBaseline(sim_options={'name':'pearson_baseline','user_based':False})
    #Start with 'normal/combination skin df'
    #df=movie_df[movie_df['normal']==1].copy()
    #raw_uid=input('type username: ')
    #filter df by preferences
    #stype=input('What is your skin type or skin problems? Type all that apply: \ndry \nsensitive \noily \nredness \ndark circles \naging \n(n if none apply):\n ')
    #ptype=input('Are you looking for any of these products? \ncleanser \nexfoliator\nmakeup-remover\ntoner \nmist \ntreatment \nserum \nlotion \nmoisturizer \nbalm \noil \nmask \npeel \nlip \neye \nsupplement \ntool:\n ')
    stype=st.multiselect("Please select all skin types and problems that apply to you:",['dry','age','dark circles','redness','sensitive','oily'])
    for s in stype:
        s.replace(' ','')
    ptype=st.multiselect("Please select all types of products you are looking for:", ['cleanser','exfoliator','makeup-removers','toner','mist','treatment','serum','lotion','moisturizer','balm','oil','mask','peel','lip','eye','supplement','tool'])
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
    return df
def new_ratings(df, raw_uid):
    rating_list = []
    #Start with 'normal/combination skin df'
    #Asking User to rate these products from their preferences
    samples=df.sample(1)
    i=1
    p=samples.prodName
    u=list(samples.url)
    #for x,y in zip(p,u):
    st.write(p)
    rating=st.selectbox('How do you rate this product on a scale of 1-5\n',range(1,6),key=i)
        #i+=1
    rating_list.append({'user':raw_uid,'url':u,'rating':rating})
    new_ratings_df=df[['user','url','rating']]
    return new_ratings_df

def recs(new_ratings_df,raw_uid):
    new_data = Dataset.load_from_df(new_ratings_df,reader)
    knn_baseline = KNNBaseline(sim_options={'name':'pearson_baseline','user_based':False})
    train, test=train_test_split(new_data, test_size=0.2, random_state=42, shuffle=True)
    knn_baseline.fit(train)
    #preds=knn_baseline.test(test)
    
    list_of_prods=[]
    for u in new_ratings_df['url'].unique():
        list_of_prods.append((u,knn_baseline.predict(raw_uid,u)[3]))
    ranked_prods = sorted(list_of_prods,key=lambda x:x[1],reverse=True)
    n=st.selectbox('How many products are you looking for?',[1,2,3,4,5,6,7,8,9,10])
    for idx, re in enumerate(ranked_prods[2:]):
        #title = df.loc[df['url'] == int(re[0])]['prodName']
        u=re[0]
        st.write('Recommendation # ',idx+1,'|| ', 'url:', 'https://www.skinstore.com/the-ordinary-aha-30-bha-2-peeling-solution-30ml/{}.html'.format(u), '||','product: ', df[df['url']==u]['prodName'].drop_duplicates(),'\n')
        n-= 1
        if n == 0:
            break

raw_uid=user()
df=get_df(df,rec)
lis=new_ratings(df,raw_uid)
recs(lis,raw_uid)

    

