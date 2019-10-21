#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 11:27:57 2019

@author: mackenziemitchell
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pickle
import pandas as pd
import plotly.graph_objs as go

with open('userratingsDF.pickle', 'rb') as f:
    dfr = pickle.load(f)
with open('CategoricalItemDF.pickle', 'rb') as f:
    full = pickle.load(f)
with open('_SENT&RATINGDF.pickle', 'rb') as f:
    df1 = pickle.load(f)
with open('recdf.pickle', 'rb') as f:
    rec = pickle.load(f)
with open('ratingsmeandf.pickle', 'rb') as f:
    fullm = pickle.load(f)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Skincare Recommender'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='rating-graph',
        figure={
            'data': [
                {'x': full['rating'].mean(), 'y': full['prodName'], 'type': 'bar','name':'Ratings'}
            ],
            
            'layout': {
                'title': 'Product v. Rating'
                }
        }
    ),
            
    dcc.Graph(
        id='rating-graph',
        figure={
            'data': [
                {'x': fullm['rating'], 'y': full['prodName'], 'type': 'bar','name':'Ratings'}
            ],
            
            'layout': {
                'title': 'Product v. Mean Rating'
                }
        }
    )
    
])

if __name__ == '__main__':
    app.run_server(debug=True)