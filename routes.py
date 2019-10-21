#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 13:40:07 2019

@author: mackenziemitchell
"""

from flask import render_template, request

from dash_package.dashboard import app

from SkincareRoutine.functions import *

@app.server.route('/dash')
def dashboard():
    return app.index()

@app.server.route('/hello')
def hello():
    return "Oh hello"


@app.server.route('/model', methods = ['GET'])
def render_html():
    return render_template('classifier.html')

@app.server.route('/model', methods = ['POST'])
def predict():
    stype = request.form.get('name')
    prediction = skin_rater(df,num,stype,ptype)
#version 1
    return str(prediction)

# version 2
   # if prediction == 0:
      # return render_template('art.html')
   # if prediction == 1:
       # return render_template('programming.html')