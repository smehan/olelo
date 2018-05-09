###########################################################
# Copyright (C) 2018 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Routing module for olelo flask web app
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs

# 3rd-party libs

# application libs
from oleloweb import app


@app.route('/')
def hello():
    return "<h1>Hello, World</h1>"
