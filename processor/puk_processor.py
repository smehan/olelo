###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Processor for transforming Proverb source xhtml into usable data
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os
import glob
import copy
import re
from collections import Counter
import pickle

# 3rd-party libs
from bs4 import BeautifulSoup, Tag
import pprint

# application libs
from grammar import HAW_POS
