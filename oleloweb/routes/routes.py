###########################################################
# Copyright (C) 2018 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Routing module for olelo flask web app
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs

# 3rd-party libs
from flask import render_template, redirect, url_for, flash
from werkzeug.contrib.cache import RedisCache

# application libs
from oleloweb import app
from processor import Puk

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


@app.route('/proverbs')
def trial():
    puk_processor = Puk(path='puk-txt')
    return render_template('list_all.html', data=puk_processor.build_proverbs())

