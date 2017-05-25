###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Processor for transforming source html into usable data
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os
import copy

# 3rd-party libs
from bs4 import BeautifulSoup, Tag
import pprint

# application libs
from grammar import HAW_POS


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

    def get_src(self) -> BeautifulSoup:
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
        hw = entry.split('\n')[0].replace('.', '').rstrip(' ')
        rest = entry.split('\n')[1:]
        return hw, rest

    @staticmethod
    def mark_haw(tag: Tag) -> str:
        """
        Takes a bs4 Tag object and returns a str with <HAW>words</HAW>
        :param tag: 
        :return: 
        """
        #tag = copy.copy(original_tag)
        for e in tag.find_all('span'):
            if e.get('lang') is None:
                continue
            elif e.get('lang') == 'HAW':
                e.insert_before('<HAW>')
                e.insert_after(('</HAW>'))
        return tag.text

    def build_entry(self, entry: Tag) -> dict:
        """
        Given a bs4 tag: entry, will parse entry and return a dict of the 
        head word and content, including ref id from processor.
        :param entry: bs4 tag object found in original source
        :return: dict: entry
        """
        # Firstly, we check to see if this is a word definition. Other cases not handled are
        # letter definition or general text
        if '.' in entry['id']:
            head_word, content = self.parse_content(entry.text)
            # need to pass a copy of entry to mark_haw to keep tag from being mutated
            _, marked_content_haw = self.parse_content(self.mark_haw(copy.copy(entry)))
            if head_word and content is not None:
                return {head_word.strip(): {'content': content,
                                            'marked_content_haw': marked_content_haw,
                                            'id': entry['id']}}

    @staticmethod
    def get_pos(s: str) -> str:
        """
        Take a string and find the HAW_POS in that string and return.
        :param s: str with definition contents: 'n. Hatband.'
        :return: 
        """
        if s is None:
            return None
        all_pos = []
        for pos, abbrevs in HAW_POS.items():
            for e in abbrevs:
                if e in s and pos not in all_pos:
                    all_pos.append(pos)
        # if there is no result for pos, mark it tbd
        if len(all_pos) == 0:
            all_pos.append('tbd')
        return all_pos

    def build_pos(self, e: dict) -> dict:
        """
        Parse an entry and get all Parts-of-speech and annotate the entry
        with the POS.
        :param e: 
        :return: 
        """
        if e is None:
            return None, None
        (hw, payload), = e.items()
        payload['pos'] = sorted([pos for item in payload['content'] for pos in self.get_pos(item)])
        return hw, payload

    def build_dict(self):
        page = self.get_src()
        refs = self.get_dict_entries(page)
        words = (self.build_entry(r) for r in refs)
        new_words = {}
        for w in words:
            hw, payload = self.build_pos(w)
            new_words.update({hw: payload})
        return new_words

if __name__ == '__main__':
    ulu_proc = Processor()
    new_dic = ulu_proc.build_dict()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(new_dic)



