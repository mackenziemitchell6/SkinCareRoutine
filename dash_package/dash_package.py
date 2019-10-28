#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 15:13:35 2019

@author: mackenziemitchell
"""

from flask import Flask
import dash

server = Flask(__name__)

server.config['DEBUG'] = True

app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')
app.config['suppress_callback_exceptions']=True

#from dash_package import routes