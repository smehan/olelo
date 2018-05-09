###########################################################
# Copyright (C) 2018 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Package initialization for olelo flask web app
###########################################################
#
#  -*- coding: utf-8 -*-

# 3rd-party libs
from flask import Flask

# application lib

######################################
# Initialization
######################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oidhirp'
# # db stuff

from oleloweb.routes import routes