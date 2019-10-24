#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 13:40:07 2019

@author: mackenziemitchell
"""

from flask import Flask, render_template, request, redirect, url_for

#from dash_package.dashboard import app
#from dash_package import app

from dash_package.dashboard import app
#from functions1 import *
from functions1 import get_samples, get_dataframe
import pandas as pd
from recfunction import Predict
import pickle

p=Predict()

with open('findf.pickle', 'rb') as f:
    rec = pickle.load(f)
#import interface.html

#server= Flask(__name__,template_folder='templates')

@app.server.route('/dash')
def dashboard():
   return app.index()

#@app.server.route('/', methods=['GET'])
#def render_html():
 #   stype=request.form.getlist('stype')
    #for s in stype:
  #  return render_template('recc_.html')
  
@app.server.route('/prefs',methods=['GET'])
def get_inputs():
        return render_template('recc_.html')
  
@app.server.route('/pref',methods=['GET'])
def new_ratings():
    stype=request.form.getlist('stype')
    df=rec[rec['normal']==1]
    df=p.get_df(stype)
    to_rate=p.ratings(df)
    #new_ratings=request.form.get('rating')
    #print(new_ratings)
    return render_template('get_ratings.html',to_rate=to_rate)

#@app.server.route('/recc',methods='POST')
#def recs():
#    new_ratings=request.args.get('rating')
 #   print(new_ratings)
    #to_rate=p.ratings(df)
   # rec_df=p.new_df(new_ratings,request.form.getlist('stype'))
    #return render_template('recc_.html' ,rec_df=rec_df)





#@app.server.route('/prefs',methods=['GET','POST'])
#def get_inputs():
 #   stype=request.form.getlist('stype')
  #  return render_template('recc_.html')
    #stype=request.form.getlist('stype')
    #if request.method == 'POST':
     #   return redirect(url_for('new_ratings'))
     #stype=request.form.getlist('stype')
      #  df=get_dataframe(stype[1:])
       # ratings=get_samples(df)
       #return render_template('recc_.html')

    
    
    

#@app.server.route('/aljfdcdc',methods=['GET','POST'])
#def make_recs():
 #   if request.method=='POST':
  #      stype=request.form.getlist('stype')
   #     raw_uid=stype[0]
    #    df=p.get_df(stype)
    #else:
     #   return render_template('get_ratings.html')


#@app.server.route('/',methods=['GET'])
#def get_ratings():
    #ratings=get_samples(df)
    #ratings=request.form.getlist('rating')
 #   return render_template('get_ratings.html')

#@app.server.route('/',methods=['GET','POST'])
#def get_ratings():
 #   if request.method == 'POST':
  #      stype=request.form.getlist('stype')
   #     ratings=get_samples(df)
   # return render_template('get_ratings.html')
        
    

#@app.server.route('/',methods=['POST'])
#def recommend():
    #stype=request.form.getlist('stype')
    #raw_uid=stype[0]
    #stype=stype[1:]
    #for s in stype:
       # pd.concat([df,rec[rec[s]==1]])
    #skin_rater(df,3,raw_uid,stype)
    #return render_template('showrecs.html')
 #   df=rec[rec['normal']==1]
   # {% for s in stype %}
       # pd.concat([df,rec[rec[s]==1]])
  #  request.form.getlist('stype')[1:]
    #skin_rater(rec,3,raw_uid,stype)
   # return render_template('showrecs.html')
    
    return render_template('new_user_recs.html')

#@app.server.route('/prediction',methods='POST')
#def make_recs():
 #   df=rec[rec['normal']==1]
  #  for s in stype:
   #     df.concat([df,rec[rec[s]==1]])
#@app.server.route('/', methods=['GET'])
#def index():
 #   if request.method == 'POST':
        #raw_uid=request.form.get('raw_uid')
  #      raw_uid=request.form.getlist('raw_uid')
   #     return render_template('recc_.html')
    #return render_template('homepg.html')  

#@app.server.route()
#def prediction():
  #  stype=request.form.getlist('stype')

#@app.route('/recommender',methods=['POST'])
#def rechtml():
    

#@app.server.route('/hello')
#def hello():
    #return "Oh hello"

#@app.route('/user_rec', methods=['POST'])
#def button1():
 #   user_name = (request.form['user_input'])
  #  best_num_player = (request.form['best_num_player'])
   # min_time = (request.form['min_time'])
    #max_time = (request.form['max_time'])
    #players = request.form.getlist('check')


#@app.server.route('/model', methods = ['GET'])
#def render_html():
#    return render_template('classifier.html')

#@app.server.route('/model', methods = ['POST'])
#def predict():
#    text = request.form.get('name')
#    prediction = classify_text(text)
#version 1
    # return str(prediction)

# version 2
   # if prediction == 0:
    #    return render_template('art.html')
    #if prediction == 1:
     #   return render_template('programming.html')