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

with open('df1.pickle', 'rb') as f:
    rec = pickle.load(f)
df=rec.loc[rec['normal']==1].copy()
def get_df(df,movie_df,stype, ptype):
    #rating_list = []
    #knn_baseline = KNNBaseline(sim_options={'name':'pearson_baseline','user_based':False})
    #Start with 'normal/combination skin df'
    #df=movie_df[movie_df['normal']==1].copy()
    #raw_uid=input('type username: ')
    #filter df by preferences
    #stype=input('What is your skin type or skin problems? Type all that apply: \ndry \nsensitive \noily \nredness \ndark circles \naging \n(n if none apply):\n ')
    #ptype=input('Are you looking for any of these products? \ncleanser \nexfoliator\nmakeup-remover\ntoner \nmist \ntreatment \nserum \nlotion \nmoisturizer \nbalm \noil \nmask \npeel \nlip \neye \nsupplement \ntool:\n ')
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
    rating=st.selectbox('How do you rate this product on a scale of 1-5\n',range(1,5),key=i)
        #i+=1
    rating_list.append({'user':raw_uid,'url':u,'rating':rating})
    new_ratings_df=df[['user','url','rating']]
    print("*****")
    print(rating_list)
    return new_ratings_df

def recs(new_ratings_df,raw_uid,n):
    new_data = Dataset.load_from_df(new_ratings_df,reader)
    knn_baseline = KNNBaseline(sim_options={'name':'pearson_baseline','user_based':False})
    train, test=train_test_split(new_data, test_size=0.2, random_state=42, shuffle=True)
    knn_baseline.fit(train)
    #preds=knn_baseline.test(test)
    
    list_of_prods=[]
    for u in new_ratings_df['url'].unique():
        list_of_prods.append((u,knn_baseline.predict(raw_uid,u)[3]))
    ranked_prods = sorted(list_of_prods,key=lambda x:x[1],reverse=True)
    
    for idx, re in enumerate(ranked_prods[2:]):
        #title = df.loc[df['url'] == int(re[0])]['prodName']
        u=re[0]
        st.write('Recommendation # ',idx+1,'|| ', 'url:', u, '||','product: ', df[df['url']==u]['prodName'].drop_duplicates(),'\n')
        n-= 1
        if n == 0:
            break

st.title("Skincare Routine Recommender")
from PIL import Image
st.image(Image.open("dash_package/static/washing-face.jpg"),width=800)

st.header("Find the Perfect Skincare Routine for your Skin Type!")
#st.info("Type your username:")
raw_uid=st.text_input("Please Enter a Username:")
st.button("Submit Username")
st.write("Please select all skin types and problems that apply to you:")
stype=[]
if st.checkbox('dry'):
    stype.append('dry')
if st.checkbox('age'):
    stype.append('age')
if st.checkbox('dark circles'):
    stype.append('darkcircles')
if st.checkbox('redness'):
    stype.append('redness')
if st.checkbox('sensitive'):
    stype.append('sensitive')
if st.checkbox('oily'):
    stype.append('oily')
    
st.button("Submit Skin Type")
st.write("Please select all types of products you are looking for:")
ptype=[]
if st.checkbox('cleanser'):
    ptype.append('cleanser')
if st.checkbox('exfoliator'):
    ptype.append('exfoliator')
if st.checkbox('makeup remover'):
    ptype.append('makeup-removers')
if st.checkbox('toner'):
    ptype.append('toner')
if st.checkbox('mist'):
    ptype.append('mist')
if st.checkbox('treatment'):
    ptype.append('treatment')
if st.checkbox('serum'):
    ptype.append('serum')
if st.checkbox('lotion'):
    ptype.append('lotion')
if st.checkbox('moisturizer'):
    ptype.append('moisturizer')
if st.checkbox('balm'):
    ptype.append('balm')
if st.checkbox('oil'):
    ptype.append('oil')
if st.checkbox('mask'):
    ptype.append('mask')
if st.checkbox('peel'):
    ptype.append('peel')
if st.checkbox('lip'):
    ptype.append('lip')
if st.checkbox('eye'):
    ptype.append('eye')
if st.checkbox('supplement'):
    ptype.append('supplement')
if st.checkbox('tool'):
    ptype.append('tool')
    
st.button("Submit Product Types")
df=get_df(df,rec,stype,ptype)
lis=new_ratings(df,raw_uid)
if st.button("Submit Rating"):
    recs(lis,raw_uid,5)
#n=st.text_input('How many products are you looking for?\n')
#recs(lis,raw_uid,5)

    

