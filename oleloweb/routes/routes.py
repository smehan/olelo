###########################################################
# Copyright (C) 2018 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Routing module for olelo flask web app
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs

# 3rd-party libs
from flask import render_template, redirect, url_for, flash

# application libs
from oleloweb import app

test_data = [
    {
        'name': 'Bob',
        'age': 55
    },
    {
        'name': 'Sue',
        'age': 44
    }
]

@app.route('/')
def hello():
    return render_template('hello.html', data=test_data)
