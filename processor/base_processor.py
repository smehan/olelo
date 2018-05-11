###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Base Processor for transforming sources into usable data
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


class BaseProcessor(object):
    """
    This class reads in the html source and readies it for parsing.
    """
    TMP_PATH = '../tmp/'

    # Regex patterns compiled here for speed
    CONTENT_POS = re.compile(r'^(?:\d+\.\s)?[a-z.]+\.')
    CONTENT_DEF = re.compile(r'^(?:\d+\.\s)?(.*)$')

    def __init__(self):
        """Constructor for Processor"""
        self.tmp_path = self.TMP_PATH

    def get_src(self, fn=None) -> BeautifulSoup:
        """
        Will read in an html document and return a bs4 object.
        :param fn:
        :return:
        """
        if fn is None:
            fn = os.path.join(self.srcpath, self.fname)
        with open(fn, 'r') as f:
            return BeautifulSoup(f.read(), 'html.parser')

    @staticmethod
    def get_dict_entries(p: BeautifulSoup) -> list:
        """
        given a bs4 object with the dictionary html, will return all of the headword elements in the page
        :param p: bs4: object formed from page
        :return: list: references to headword elements in page as bs4 tags
        """
        if not isinstance(p, BeautifulSoup):
            raise TypeError(f'{p}: {type(p)} needs to be :BeautifulSoup')
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
        hw = entry.split('\n')[0].rstrip()
        rest = entry.split('\n')[1:]
        return hw, rest

    def prepare_source(self, fn=None):
        """
        Read in source html, parse the html and
        return a generator for all entries in the source
        :param fn: str containg the basename of file to read
        :return: generator
        """
        page = self.get_src(fn)
        refs = self.get_dict_entries(page)
        return (self.build_source_entry(r) for r in refs)


if __name__ == '__main__':
    print(f"{__file__} is not meant to be run but rather inherited...")