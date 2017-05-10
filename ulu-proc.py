###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Processor for transforming source html into usable data
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os

# 3rd-party libs
from bs4 import BeautifulSoup

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
            return BeautifulSoup(f.read(), 'html.parser')

    @staticmethod
    def get_dict_entries(p):
        """
        given a bs4 object with the dictionary html, will return all of the dictionary elements in the page
        :param p: bs4 object of page
        :return: all dictionary elements in page
        """
        for d in page.find_all("div"):
            if 'id' in d.attrs:
                print(d)


if __name__ == '__main__':
    ulu_proc = Processor()
    page = ulu_proc.get_src()
    ulu_proc.get_dict_entries(page)