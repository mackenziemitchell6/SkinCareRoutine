#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 11:41:11 2019

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
    html.H1(children='Skincare Products EDA Visuals'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='rating-graph',
        figure={
            'data': [
                {'x': full['rating'], 'y': full['prodName'], 'type': 'bar','name':'Ratings'}
            ],
            
            'layout': {
                'title': 'Product v. Rating'
                }
        }
    ),
    
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=full[full['brand'] == i]['rating'],
                    y=full[full['brand'] == i]['price'],
                    text=full[full['brand'] == i]['brand'],
                    mode='markers',
                    opacity=0.65,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in full.brand.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'Rating'},
                yaxis={'title': 'Price'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    
    dcc.Graph(
        id='ratingcount-graph',
        figure={
            'data': [
                {'x': fullm['rating_count'].mean(), 'y': fullm['rating'], 'type': 'scatter','name':'Ratings'}
            ],
            
            'layout': {
                'title': 'Rating v. RatingCount'
                }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)