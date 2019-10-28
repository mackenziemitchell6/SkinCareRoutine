#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 17:13:12 2019

@author: mackenziemitchell
"""

mkdir -p -/streamlit/

echo "\
[general]\n\
email = \"mackenziemitchell6@gmail.com\"\n\
" > ~/.stramlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml