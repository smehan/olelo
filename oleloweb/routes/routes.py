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
from hua import Hua


@app.route('/')
@app.route('/hua/wotd')
def wotd():
    hua = Hua()
    return render_template('hua/hua.html', wotd=hua.make_word_of_day())


@app.route('/proverbs')
def list_all_proverbs():
    puk_processor = Puk(path='puk-txt')
    return render_template('proverbs/list_all_proverbs.html', data=puk_processor.build_proverbs())


