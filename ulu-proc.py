###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Processor for transforming source html into usable data
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os
import string

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
        with open(os.path.join(self.ULUDICTSRCPATH, 'puk-1.html'), 'r') as f:
            return BeautifulSoup(f.read(), 'html.parser')

    @staticmethod
    def get_dict_entries(p):
        """
        given a bs4 object with the dictionary html, will return all of the dictionary elements in the page
        :param p: bs4 object formed from page
        :return: list of references to dictionary elements in page as bs4 tags
        """
        elements = []
        for d in page.find_all("div"):
            if 'id' in d.attrs:
                elements.append(d)
        return elements

    @staticmethod
    def parse_content(entry):
        """
        method to parse and extract the head word and 
        definitions from the entry.
        :param entry: string from original page source entry
        :return: string of head word, string of content
        """
        if entry is None or entry == '':
            return None
        entry = entry.strip()
        hw = entry.split('\n')[0].replace('.', '').rstrip(' ')
        rest = entry.split('\n')[1:]
        return hw, rest

    @staticmethod
    def build_entry(entry):
        """
        Given an entry bs4 tag, will parse entry and return a dict of the 
        target word and content, including ref id from src.
        :param entry: bs4 tag found in original source
        :return: dict of entry
        """
        # Firstly, we check to see if this is a word definition. Other cases are
        # letter definition or general text
        if '.' in entry['id']:
            head_word, content = ulu_proc.parse_content(entry.text)
            out = {head_word: {'content': content, 'id': entry['id'] }}
            return out


if __name__ == '__main__':
    ulu_proc = Processor()
    page = ulu_proc.get_src()
    refs = ulu_proc.get_dict_entries(page)
    for r in refs:
        print(ulu_proc.build_entry(r))
