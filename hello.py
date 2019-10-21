#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 16:37:11 2019

@author: mackenziemitchell
"""

from flask import Flask
app=Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
