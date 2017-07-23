###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Converts a 24hr formate time string into equivalent word statements in hawaiian.
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os
import datetime as dt
import re

# 3rd-party libs

# application libs

words_dict = {1: 'ʻekahi', 2: 'ʻelua', 3: 'ʻekolu', 4: 'ʻehā', 5: 'ʻelima',
              6:'ʻeono', 7: "ʻehiku", 8: "ʻewalu", 9: "ʻeiwa", 10: "ʻumi",
              11: "ʻumikūmākahi", 12: "ʻumikūmālua", 13: "ʻumikūmākolu", 14: "ʻumikūmāhā", 15: "ʻumikūmālima",
              16: "ʻumikūmāono", 17: "ʻumikūmāhika", 18: "ʻumikūmāwalu", 19: "ʻumikūmāiwa",
              20: "iwakālua", 21: "iwakālua-kūmā-kahi", 22: "iwakālua-kūmā-lua",
              23: "iwakālua-kūmā-kolu", 24: "iwakālua-kūmā-hā", 25: "iwakālua-kūmā-lima",
              26: "iwakālua-kūmā-ono", 27: "iwakālua-kūmā-hiku", 28: "iwakālua-kūmā-walu",
              29: "iwakālua-kūmā-iwa"}


def time_to_words(ts: str):
    try:
        return parse_time(ts)
    except AttributeError as e:
        raise ValueError(f"{ts} must be either a hh:mm time or now...")


def parse_time(s: str):
    try:
        m = re.match("(\d\d):(\d\d)|now", s)
    except AttributeError as e:
        raise e
    if m.group(2) is not None:
        return m.group(1), m.group(2)
    else:
        now = dt.datetime.now().strftime("%H:%M")
        return parse_time(now)


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