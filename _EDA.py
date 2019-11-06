#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 12:21:24 2019

@author: mackenziemitchell
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from RecFunctions import type_prod_histogram, type_problem_histogram

with open('pickles/df1.pickle', 'rb') as f:
    df = pickle.load(f)
    
df.groupby(['brandName']).mean()

plt.figure(figsize=(8,6))
sns.distplot(df.rating)
plt.title('All Ratings Distribution')

#Brands Distribution
plt.figure(figsize=(40,40))
df.groupby(['brandName']).mean().index.value_counts().plot(kind='pie', autopct='%1.0f%%')
plt.savefig('Visuals/VennDiagram_AllBrands.png')

#Ratings Distribution
plt.figure(figsize=(8,8))
sns.distplot(df.rating)
plt.title('All Ratings Distribution')
plt.ylabel('Density')
plt.savefig('Visuals/AllRatingsDistribution.png')

#Prices Distribution
plt.figure(figsize=(8,8))
sns.distplot(df.price)
plt.title('All Prices Distribution')
plt.ylabel('Density')
plt.savefig('Visuals/AllPricesDistribution.png')

#Examining overlaps of types of products/skin problems in products
type_problem_histogram(df,'allData')
type_prod_histogram(df,'allData')

type_problem_histogram(df[df['age']==1],'age')
type_prod_histogram(df[df['age']==1],'age')

type_problem_histogram(df[df['darkcircles']==1],'darkCircles')
type_prod_histogram(df[df['darkcircles']==1],'darkCircles')

type_problem_histogram(df[df['acne']==1],'acne')
type_prod_histogram(df[df['acne']==1],'acne')

type_problem_histogram(df[df['dry']==1],'dry')
type_prod_histogram(df[df['dry']==1],'dry')

type_problem_histogram(df[df['redness']==1],'redness')
type_prod_histogram(df[df['redness']==1],'redness')

type_problem_histogram(df[df['sensitive']==1],'sensitive')
type_prod_histogram(df[df['sensitive']==1],'sensitive')

type_problem_histogram(df[df['oily']==1],'oily skin')
type_prod_histogram(df[df['oily']==1],'oily skin')

type_problem_histogram(df[df['normal']==1],'normal skin')
type_prod_histogram(df[df['normal']==1],'normal skin')

type_problem_histogram(df[df['cleanser']==1],'cleanser')
type_prod_histogram(df[df['cleanser']==1],'cleanser')

type_problem_histogram(df[df['oil']==1],'oil')
type_prod_histogram(df[df['oil']==1],'oil')

#No matter what problem someone has, everyone should use an exfoliator!!
type_problem_histogram(df[df['exfoliator']==1],'exfoliator')
type_prod_histogram(df[df['exfoliator']==1],'exfoliator')

type_problem_histogram(df[df['makeup-removers']==1],'makeup remover')
type_prod_histogram(df[df['makeup-removers']==1],'makeup remover')

#No matter what skin problem, everyone should use a toner!!
type_problem_histogram(df[df['toner']==1],'toner')
type_prod_histogram(df[df['toner']==1],'toner')

type_problem_histogram(df[df['mist']==1],'mist')
type_prod_histogram(df[df['mist']==1],'mist')

type_problem_histogram(df[df['treatment']==1],'treatment')
type_prod_histogram(df[df['treatment']==1],'treatment')

type_problem_histogram(df[df['serum']==1],'serum')
type_prod_histogram(df[df['serum']==1],'serum')

type_problem_histogram(df[df['lotion']==1],'lotion')
type_prod_histogram(df[df['lotion']==1],'lotion')

type_problem_histogram(df[df['moisturizer']==1],'moisturizer')
type_prod_histogram(df[df['moisturizer']==1],'moisturizer')

type_problem_histogram(df[df['balm']==1],'balm')
type_prod_histogram(df[df['balm']==1],'balm')

type_problem_histogram(df[df['mask']==1],'mask')
type_prod_histogram(df[df['mask']==1],'mask')

type_problem_histogram(df[df['peel']==1],'peel')
type_prod_histogram(df[df['peel']==1],'peel')

type_problem_histogram(df[df['lip']==1],'lip')
type_prod_histogram(df[df['lip']==1],'lip')

type_problem_histogram(df[df['eye']==1],'eye')
type_prod_histogram(df[df['eye']==1],'eye')

type_problem_histogram(df[df['supplement']==1],'supplement')
type_prod_histogram(df[df['supplement']==1],'supplement')

type_problem_histogram(df[df['tool']==1],'tool')
type_prod_histogram(df[df['tool']==1],'tool')

#no makeup-removers that help with anti-aging
plt.figure(figsize=(5,5))
sns.scatterplot(x='makeup-removers',y='age',data=df)
#no makeup-removers that help with darkcircls
plt.figure(figsize=(5,5))
sns.scatterplot(x='makeup-removers',y='darkcircles',data=df)
#no makeup removers that help with redness
plt.figure(figsize=(5,5))
sns.scatterplot(x='makeup-removers',y='redness',data=df)
#no mists that help with acne
plt.figure(figsize=(5,5))
sns.scatterplot(x='mist',y='acne',data=df)
#no balms that help with acne
plt.figure(figsize=(5,5))
sns.scatterplot(x='balm',y='acne',data=df)
#no lip-care products that help with acne
plt.figure(figsize=(5,5))
sns.scatterplot(x='lip',y='acne',data=df)
#no peels that help with redness
plt.figure(figsize=(5,5))
sns.scatterplot(x='peel',y='redness',data=df)
#no supplements that help with redness
plt.figure(figsize=(5,5))
sns.scatterplot(x='supplement',y='redness',data=df)
#no supplements that help with sensitive skin
plt.figure(figsize=(5,5))
sns.scatterplot(x='supplement',y='sensitive',data=df)
#no supplements that help with normal/combination skin
plt.figure(figsize=(5,5))
sns.scatterplot(x='supplement',y='normal',data=df)
