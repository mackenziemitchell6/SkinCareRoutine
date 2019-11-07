#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 18:34:27 2019

@author: mackenziemitchell
"""

mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless=true\n\
port= $PORT\n\
enableCORS=false\n\
\n\
" > ~/.streamlit/config.toml