###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Processor for transforming source html into usable data
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os

# 3rd-party libs
import bs4

# application libs


class Processor(object):
    """
    This class reads in the html source of the dict and transforms it into usable string encoded data.
    """
    ULUDICTSRCPATH = 'ulu-dict/'

    def __init__(self,):
        """Constructor for Processor"""

    def get_src(self):
        with open(os.path.join(self.ULUDICTSRCPATH, 'ulukau-1.html'), 'r') as f:
            print(f.readlines())


if __name__ == '__main__':
    ulu_proc = Processor()
    ulu_proc.get_src()
