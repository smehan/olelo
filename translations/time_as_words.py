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
        return form_words(*parse_time(ts))
    except AttributeError as e:
        raise ValueError(f"{ts} must be either a hh:mm time or now...")


def parse_time(s: str):
    """
    Extracts hour and minute values or computes those values for
    now.
    :param s: 24hr clock or "now"
    :return: Tuple with (hour, minute) of time.
    """
    try:
        m = re.match("(\d\d):(\d\d)|now", s)
    except AttributeError as e:
        raise e
    if m.group(2) is not None:
        return int(m.group(1)), int(m.group(2))
    else:
        now = dt.datetime.now().strftime("%H:%M")
        return parse_time(now)


def fmt_minutes(h: int, m: int):
    if m < 16:
        words = ''
    elif m < 46:
        words = ' hapalua '
    else:
        words = ''
        h += 1
    return h, words


def fmt_hours(h: int):
    if h < 5:
        return f"{words_dict[h]}" + " kēia o ka ʻaumoe" # 23-05
    elif h < 6:
        return f"{words_dict[h]}" + " kēia o ka wanaʻao" # 05 - 06
    elif h < 10:
        return f"{words_dict[h]}" + " kēia o ke kakahiaka" # 06 - 10
    elif h < 14:
        return f"{words_dict[h]}" + " kēia o ke awakea" # 10 - 14
    elif h < 17:
        return f"{words_dict[h]}" + " kēia o ka ʻauinalā" # 14 - 17
    elif h < 20:
        return f"{words_dict[h]}" + " kēia o ke ahiahi" # 17 - 20
    elif h < 23:
        return f"{words_dict[h]}" + " kēia o ka pō" # 20 - 23
    else:
        return f"{words_dict[h]}" + " kēia o ka ʻaumoe" # 23 - 05


def form_words(hh: int, mm: int):
    hh, minutes_part = fmt_minutes(hh, mm)
    return f'ʻO ka {minutes_part} hola {fmt_hours(hh)}.'.replace('  ', ' ')
