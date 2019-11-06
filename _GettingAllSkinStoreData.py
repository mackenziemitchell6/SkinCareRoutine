#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 12:16:58 2019

@author: mackenziemitchell
"""

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import pickle
from RecFunctions import get_products_by_type,get_products_by_problem, categorical_columns, type_column

#Functions Scrape Data and Get Info Df's For SkinStore

cleansers=get_products_by_type('cleansers',14)
exfoliators=get_products_by_type('exfoliators',6)
removers=get_products_by_type('makeup-removers',3)
toners=get_products_by_type('toners',6)
mists=get_products_by_type('mists',3)
treatments=get_products_by_type('treatments',14)
serums=get_products_by_type('serums',16)
lotions=get_products_by_type('lotions',6)
moisturizers=get_products_by_type('moisturizers',23)
balms=get_products_by_type('balms',3)
oils=get_products_by_type('oils',5)
masks=get_products_by_type('masks',9)
peels=get_products_by_type('peels',3)
lips=get_products_by_type('lip-care',4)
eyes=get_products_by_type('eye-care',9)
supplements=get_products_by_type('supplements',1)
tools=get_products_by_type('tools',5)

acnedf,acne = get_products_by_problem('acne-blemishes',10)
agedf,age = get_products_by_problem('anti-aging',30)
darkcdf,darkcircles = get_products_by_problem('dark-circles',5)
drydf,dryness = get_products_by_problem('dry-skin',19)
ncdf,norm= get_products_by_problem('normal-combination',17)
oilydf,oily=get_products_by_problem('oily-skin',17)
sensitivedf,sensi=get_products_by_problem('sensitive-skin',17)
reddf,redness=get_products_by_problem('redness-rosacea',17)

braa=[]
ratee=[]
pri=[]
ur=[]
imgs=[]
for i,r,p,u in zip(acnedf.prodName,acnedf.rating,acnedf.price,acnedf.url):
    braa.append(i)
    ratee.append(r)
    pri.append(p)
    ur.append(u)
for i,r,p,u in zip(agedf.prodName,agedf.rating,agedf.price,agedf.url):
    braa.append(i)
    ratee.append(r)
    pri.append(p)
    ur.append(u)
for i,r,p,u in zip(darkcdf.prodName,darkcdf.rating,darkcdf.price,darkcdf.url):
    braa.append(i)
    ratee.append(r)
    pri.append(p)
    ur.append(u)
for i,r,p,u in zip(drydf.prodName,drydf.rating,drydf.price,drydf.url):
    braa.append(i)
    ratee.append(r)
    pri.append(p)
    ur.append(u)
for i,r,p,u in zip(ncdf.prodName,ncdf.rating,ncdf.price,ncdf.url):
    braa.append(i)
    ratee.append(r)
    pri.append(p)
    ur.append(u)
for i,r,p,u in zip(oilydf.prodName,oilydf.rating,oilydf.price,oilydf.url):
    braa.append(i)
    ratee.append(r)
    pri.append(p)
    ur.append(u)
for i,r,p,u in zip(sensitivedf.prodName,sensitivedf.rating,sensitivedf.price,sensitivedf.url):
    braa.append(i)
    ratee.append(r)
    pri.append(p)
    ur.append(u)
for i,r,p,u in zip(reddf.prodName,reddf.rating,reddf.price,reddf.url):
    braa.append(i)
    ratee.append(r)
    pri.append(p)
    ur.append(u)
datadict=[]
for i,r,p,u in zip(braa,ratee,pri,ur):
    datadict.append({'prodName':i,'rating':r,'price':p,'url':u})
finaldf=pd.DataFrame(datadict)

finaldf.rating=[float(i) for i in finaldf.rating]
finaldf.price=[float(i) for i in finaldf.price]

#Finalize Full DF
categorical_columns('age',age,finaldf)
categorical_columns('darkcircles',darkcircles,finaldf)
categorical_columns('acne',acne,finaldf)
categorical_columns('dry',dryness,finaldf)
categorical_columns('redness',redness,finaldf)
categorical_columns('sensitive',sensi,finaldf)
categorical_columns('oily',oily,finaldf)
categorical_columns('normal',norm,finaldf)
categorical_columns('cleanser',cleansers,finaldf)
categorical_columns('exfoliator',exfoliators,finaldf)
categorical_columns('makeup-removers',removers,finaldf)
categorical_columns('toner',toners,finaldf)
categorical_columns('mist',mists,finaldf)
categorical_columns('treatment',treatments,finaldf)
categorical_columns('serum',serums,finaldf)
categorical_columns('lotion',lotions,finaldf)
categorical_columns('moisturizer',moisturizers,finaldf)
categorical_columns('balm',balms,finaldf)
categorical_columns('oil',oils,finaldf)
categorical_columns('mask',masks,finaldf)
categorical_columns('peel',peels,finaldf)
categorical_columns('lip',lips,finaldf)
categorical_columns('eye',eyes,finaldf)
categorical_columns('supplement',supplements,finaldf)
categorical_columns('tool',tools,finaldf)

# with open('pickles/findf.pickle', 'wb') as f:
#     pickle.dump(finaldf, f, pickle.HIGHEST_PROTOCOL)

#Get Review Info & Get Into DF

ratingdict=[]
for u in finaldf.url:
    response=requests.get('https://www.skinstore.com/the-ordinary-aha-30-bha-2-peeling-solution-30ml/{}.html'.format(u))
    soup=BeautifulSoup(response.content,'html.parser')
    titles=soup.findAll('h3',{'class':'productReviews_topReviewTitle'})
    ratings=soup.findAll('div',{'class':'productReviews_topReviewsRatingStarsContainer'})
    contents=soup.findAll('p',{'class':'productReviews_topReviewsExcerpt'})
    dates=soup.findAll('span',{'data-js-element':'createdDate'})
    users=soup.findAll('div',{'class':'productReviews_footerDateAndName'})
    brands=soup.find('div',{'data-information-component':'brand'})
    products=soup.find('h1',{'data-product-name':'title'})
    for t,r,c,d,i in zip(titles,ratings,contents,dates,users):
        ratingdict.append({'url':u,'brandName':brands.text.replace('\n',''),'prodName':products.text,'title':t.text.replace('\n',''),'rating':str(r).split('aria-label=')[1][1:2],'content':c.text.replace('\n','').replace('\r',''),'date':d.text,'user':i.text.replace('\n','').split('by')[1].lower()})
ratingdf=pd.DataFrame(ratingdict)
ratingdf['rating']=[int(r) for r in ratingdf['rating']]
ratingdf.user=ratingdf.user.replace('','user')
ratingdf['brandName']=[r.replace('\n','') for r in ratingdf['brandName']]
ratingdf.drop_duplicates(inplace=True)
ratingdf.content=[c.lower() for c in ratingdf.content]
ratingdf['date']=pd.to_datetime(ratingdf.date)
finaldf.drop(columns='rating',inplace=True)
final=pd.merge(finaldf,ratingdf, on='url')
final.drop(columns=['prodName_y'],inplace=True)
final.rename(columns={'prodName_x':'prodName'},inplace=True)

#Saving Final DF for Customized Rec Engine

with open('df1.pickle', 'wb') as f:
    pickle.dump(final, f, pickle.HIGHEST_PROTOCOL)
