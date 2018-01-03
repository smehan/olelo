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
from collections import defaultdict
import pprint

# application libs
from grammar import HAW_POS


class Processor(object):
    """
    This class reads in the html source of the dict and transforms it into usable string: encoded data.
    """
    PUK_PROV_SRC_PATH = '../puk-txt/'
    PUK_PROV_SRC_FILES = 'chapter\d\d.html'
    TMPPATH = '../tmp/'

    # Regex patterns compiled here for speed
    CONTENT_POS = re.compile(r'^(?:\d+\.\s)?[a-z.]+\.')
    CONTENT_DEF = re.compile(r'^(?:\d+\.\s)?(.*)$')

    def __init__(self, path=None, names=None):
        """Constructor for Processor"""
        if path is None:
            self.srcpath = self.PUK_PROV_SRC_PATH
        elif path:
            self.srcpath = path
        # TODO this will break for more than one file passed as a param
        if names is None:
            self.fname = self.PUK_PROV_SRC_FILES
        elif names:
            self.fname = names

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
    def get_puk_entries(p: BeautifulSoup) -> list:
        """
        given a bs4 object with the puk html, will return all of the proverb entries in the file
        :param p: bs4: object formed from page
        :return: list: each element is a proverb, followed by transalation, followed by explanation
        """
        if not isinstance(p, BeautifulSoup):
            raise TypeError(f'{p}: {type(p)} needs to be :BeautifulSoup')
        elements = []
        for e in p.find_all("p"):
            if ['image'] not in e.attrs.values():
                elements.append(e)
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
        refs = self.get_puk_entries(page)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(refs)
        self.split_entries(refs)
        #return (self.build_source_entry(r) for r in refs)

    @staticmethod
    def split_entries(doc: list):
        """
        Given a doc with lines from html source, split the lines into
        dict entries for each proverb.
        :param doc:
        :return:
        """
        out = defaultdict(list)
        for r in doc:
            print(r)
        return out


    def build_source_entry(self, tag: Tag) -> dict:
        """
        Given a bs4 tag will parse tag and return a dict of the
        head word and content, including ref id.
        :param tag: bs4 tag object found in original source
        :return: dict: entry
        """
        # Firstly, we check to see if this is a word definition. Other cases not handled are
        # letter section declaration or general text
        if '.' in tag['id']:
            head_word, content = self.parse_content(tag.text)
            # need to pass a copy of tag to mark_haw to keep tag from being mutated
            _, marked_content_haw = self.parse_content(self.mark_haw(copy.copy(tag)))
            if head_word and content is not None:
                return {head_word.replace('.', '').strip(): {'content': content,
                                                             'marked_content_haw': marked_content_haw,
                                                             'hw_stress': head_word.strip(),
                                                             'id': [tag['id']]}}


if __name__ == '__main__':
    puk_processor = Processor(names='chapter02.html')
    refs = puk_processor.prepare_source()