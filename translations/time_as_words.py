###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Converts a 24hr formate time string into equivalent word statements in hawaiian.
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os
import datetime.datetime

# 3rd-party libs

# application libs

words_dict = {1: 'ekahi', 2: 'elua', 3: 'e', 4: '', 5: '',
              6:'', 7:'', 8:'', 9:'', 10:'',
              11:'', 12:'', 13:'', 14:'', 15:'',
              16:'', 17:'', 18:'', 19:'', 20:'',
              21:'', 22:'', 23:'', 24:'', 25:'',
              26:'', 27:'', 28:'', 29:''}

def time_to_words():
    pass

def time_conversion(words_dict, hours, minutes, period):
    """Return time as words
    based on relevant condition"""
    if hours == 12:
        hours2 = words_dict.get(1)
    else:
        hours2 = words_dict.get(hours+1)
    if hours == 12 and minutes == 0 and period == 'before midday':
        time_words = 'Midnight'
    elif hours == 12 and minutes == 0 and period == 'after midday':
        time_words = 'Midday'
    elif minutes == 0:
        time_words = "{0} o'clock {1}.".format(str(words_dict.get(hours)).title(),
                                               period)
    elif minutes == 15:
        time_words = "Quarter past {0} {1}.".format(words_dict.get(hours),
                                                    period)
    elif minutes == 30:
        time_words = "Half past {0} {1}.".format(words_dict.get(hours),
                                                 period)
    elif minutes == 45:
        time_words = "Quarter to {0} {1}.".format(hours2,
                                                  period)
    elif minutes < 30:
        min_str = words_dict.get(minutes).capitalize()
        min_num = "" if minutes == 1 else "s"
        time_words = "{0} minute{1} past {2} {3}.".format(min_str,
                                                          min_num,
                                                          words_dict.get(hours),
                                                          period)
    else:
        min_str = words_dict.get(60 - minutes).capitalize()
        min_num = "" if 60 - minutes == 1 else "s"
        time_words = '{0} minute{1} to {2} {3}.'.format(min_str,
                                                        min_num,
                                                        hours2,
                                                        period)
    return time_words