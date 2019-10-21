#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 13:45:11 2019

@author: mackenziemitchell
"""

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Label('Please Select Your Skin Type(s):'),
    dcc.Checklist(
        id='skintype-checklist',
        options=[
            {'label': 'Normal/Combination', 'value': 'normal'},
            {'label': 'Dry', 'value': 'dry'},
            {'label': 'Sensitive', 'value': 'sensitive'},
            {'label': 'Redness', 'value': 'redness'},
            {'label': 'Oily', 'value': 'oily'},
            {'label': 'Dark Circles', 'value': 'darkcircles'},
            {'label': 'Aging', 'value': 'aging'},
        ],
        value=['normal']
    ),
    html.Label('Please Select the Type(s) of Product(s) You Are Looking For:'),
    dcc.Checklist(
        id='prodtype-checklist',
        options=[
            {'label': 'Cleanser', 'value': 'cleanser'},
            {'label': 'Exfoliator', 'value': 'exfoliator'},
            {'label': 'Makeup Remover', 'value': 'makeup-removers'},
            {'label': 'Toner', 'value': 'toner'},
            {'label': 'Mist', 'value': 'mist'},
            {'label': 'Treatment', 'value': 'treatment'},
            {'label': 'Serum', 'value': 'serum'},
            {'label': 'Moisturizer', 'value': 'moisturizer'},
            {'label': 'Balm', 'value': 'balm'},
            {'label': 'Oil', 'value': 'oil'},
            {'label': 'Mask', 'value': 'mask'},
            {'label': 'Peel', 'value': 'peel'},
            {'label': 'Lip', 'value': 'lip'},
            {'label': 'Eye', 'value': 'eye'},
            {'label': 'Supplement', 'value': 'supplement'},
            {'label': 'Tool', 'value': 'tool'},
        ],
        value=['cleanser','makeup-removers','toner','moisturizer']
    ),
])
@app.callback(
    dash.dependencies.Output('skintype-checklist', 'options'),
    [dash.dependencies.Input('skintype-checklist', 'value')])
def set_skin_type(selected_type):
    return (selected_type)

if __name__ == '__main__':
    app.run_server(debug=True)
