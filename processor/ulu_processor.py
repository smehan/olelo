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
    This class reads in the html source of the dict and transforms it into usable string: encoded data.
    """
    ULUDICTSRCPATH = '../ulu-dict/'
    ULUDICTSRCFILES = 'puk-1.html'

    def __init__(self, path=None, names=None):
        """Constructor for Processor"""
        if path is None:
            self.srcpath = self.ULUDICTSRCPATH
        elif path:
            self.srcpath = path
        # TODO this will break for more than one file passed as a param
        if names is None:
            self.fname = self.ULUDICTSRCFILES
        elif names:
            self.fname = names

    def get_src(self):
        with open(os.path.join(self.srcpath, self.fname), 'r') as f:
            return BeautifulSoup(f.read(), 'html.parser')

    @staticmethod
    def get_dict_entries(p: BeautifulSoup) -> list:
        """
        given a bs4 object with the dictionary html, will return all of the headword elements in the page
        :param p: bs4: object formed from page
        :return: list: references to headword elements in page as bs4 tags
        """
        if not isinstance(p, BeautifulSoup):
            raise TypeError
        elements = []
        for d in p.find_all("div"):
            if 'id' in d.attrs:
                elements.append(d)
        return elements

    @staticmethod
    def parse_content(entry: str) -> (str, str):
        """
        method to parse and extract the head word and 
        definitions from the entry.
        :param entry: string from original page source entry
        :return: string: head word, string: content
        """
        if entry is None or entry == '':
            return None, None
        entry = entry.strip()
        # TODO there are language tags in the original html, including HAW and LAT, that prolly should be leveraged
        hw = entry.split('\n')[0].replace('.', '').rstrip(' ')
        rest = entry.split('\n')[1:]
        return hw, rest

    @staticmethod
    def build_entry(entry: BeautifulSoup) -> dict:
        """
        Given an entry bs4 tag, will parse entry and return a dict of the 
        head word and content, including ref id from processor.
        :param entry: bs4: tag found in original source
        :return: dict: entry
        """
        # Firstly, we check to see if this is a word definition. Other cases not handled are
        # letter definition or general text
        if '.' in entry['id']:
            head_word, content = ulu_proc.parse_content(entry.text)
            if head_word and content is not None:
                return {head_word: {'content': content, 'id': entry['id'] }}


if __name__ == '__main__':
    ulu_proc = Processor()
    page = ulu_proc.get_src()
    refs = ulu_proc.get_dict_entries(page)
    for r in refs:
        print(ulu_proc.build_entry(r))

