#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 15:58:06 2019

@author: mackenziemitchell
"""

<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
      integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T"
      crossorigin="anonymous"
    />
    <title>Skincare Routine Recommender</title>

<style>
h1{color: #FF5700}
h3{color: #ff9933}
.content {
  max-width: 500px;
  margin: auto;
}
.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;
}
</style>

  </head>
  <body>

    <img src="{{url_for('static', filename='title.png')}}" alt="lol" width="800" class="center"/>

    <h1 style="text-align:center;">text classifier!!!</h1>

    <h3 style="text-align:center;">input some words below to see if your text is more art or programming:</h3>

    <form method="POST" style="text-align:center;">
                    <input type="text" name="name" width="800"><br>
                    <input type="submit" value="submit"><br>
    </form>

    <a class="nav-item nav-link text-muted" href="dash">Dashboard</a>

  </body>
</html>