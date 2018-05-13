###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Utils for working with Hawaiian language and strings.
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import unicodedata

# 3rd-party libs

# application libs


def unicode_code_points(s):
    """
    Return the unicode code points for each symbol in 
    a unicode string.
    :param s: string to return code points for
    :return: 
    """
    for i, c in enumerate(s):
        print(f'{i} {ord(c):04x} {unicodedata.category(c)}', end=' ')
        print(unicodedata.name(c))


if __name__ == '__main__':
    s = 'a iʻole'
    unicode_code_points(s)