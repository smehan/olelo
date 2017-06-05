###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Processor for transforming source html into usable data
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os
import copy
import re
from collections import Counter
import pickle

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
    TMPPATH = '../tmp/'

    # Regex patterns compiled here for speed
    CONTENT_POS = re.compile(r'^(?:\d+\.\s)?[a-z/A-Z]+\.')
    CONTENT_DEF = re.compile(r'')

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
        for e in tag.find_all('span'):
            if e.get('lang') is None:
                continue
            elif e.get('lang') == 'HAW':
                e.insert_before('<HAW>')
                e.insert_after(('</HAW>'))
        return tag.text

    # TODO this is a stub
    def build_cfs(self):
        """
        Take a tag and build a representation of Cf. entries in the content.
        This will be of form 'Cf. haw_word; ...; haw_word.'
        :return: 
        """
        pass

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

    def get_pos(self, s: str) -> str:
        """
        Take a string and find the HAW_POS in that string and return.
        :param s: str with definition contents: 'n. Hatband.'
        :return: 
        """
        if s is None:
            return None
        all_pos = []
        try:
            s = re.match(self.CONTENT_POS, s).group(0)
        except AttributeError:
            print(f'No part of speech for {s}')
            return all_pos
        for pos, abbrevs in HAW_POS.items():
            for e in abbrevs:
                if e in s and pos not in all_pos:
                    all_pos.append(pos)
        # if there is no result for pos, mark it tbd
        if len(all_pos) == 0:
            all_pos.append('tbd')
        return all_pos

    def build_pos(self, contents: list) -> list:
        """
        Parse an entry and return all Parts-of-speech.
        :param contents: list
        :return: list ['noun', 'verb', ...]
        """
        if contents is None:
            return None
        return sorted([pos for item in contents for pos in self.get_pos(item)])

    def get_def(self, s: str) -> str:
        """
        Parse a contents string and extract the definition text.
        :param s: an element of contents in source_dict
        :return: 
        """
        if s is None:
            return None
        try:
            parts = re.split(self.CONTENT_POS, s)
        except TypeError:
            raise TypeError(f'Type error on splitting {s}')
        # got a good string after splitting on pos
        if len(parts) > 1 and parts[1] != '':
            return parts[1].strip()
        # if still two parts, then there was only a pos in the line...
        elif len(parts) > 1:
            return None
        # otherwise, there was text with no pos
        else:
            # assume that line begins with a digit and .
            return parts[0].split('.', 1)[1].strip()

    def build_defs(self, contents: list) -> dict:
        """
        Parse an entry and return all definitions added as a sub-dict.
        :param contents: list
        :return: dict {'defs': {'1': 'text here', ...}
        """
        if contents is None or len(contents) == 0:
            return None
        def_dict = {}
        # if len(contents) == 1:
        #     def_dict['defs'] = {'1': self.get_def(contents[0])}
        def_count = 0
        for i, _ in enumerate(contents):
            s = self.get_def(contents[i])
            if s is not None:
                def_count += 1
                def_dict[str(def_count)] = s
        return def_dict

    def build_parts(self, e: dict) -> dict:
        """
        For each entry, build out components of parsed dictionary entry, 
        including pos, definitions,
        payload is a dict containing all components.
        :param e: 
        :return: 
        """
        if e is None:
            return None, None
        (hw, payload), = e.items()
        payload['pos'] = self.build_pos(payload['content'])
        payload['defs'] = self.build_defs(payload['content'])
        return hw, payload

    def prepare_source(self):
        """
        Read in source html, parse the html and 
        build a generator for all entries in the source
        :return: generator
        """
        page = self.get_src()
        refs = self.get_dict_entries(page)
        return (self.build_entry(r) for r in refs)

    def make_dict(self, source_dict: dict) -> dict:
        """
        Take the parsed entries from html source and 
        form a dict with appropriate attrs.
        :param source_dict: 
        :return: 
        """
        output = {}
        for entry in source_dict:
            hw, rest = self.build_parts(entry)
            output.update({hw: rest})
        return output

    def build_dict(self) -> dict:
        """
        reads in source html and outputs a dict with all entries.
        Includes a serialized object on disk.
        :return: 
        """
        words = self.prepare_source()
        new_words = self.make_dict(words)
        # ensure that there are no Nones in the dict
        while new_words.get('None'):
            new_words.pop(None)
        with open(os.path.join(self.TMPPATH, 'new_words.pickle'), 'wb') as fh:
            pickle.dump(new_words, fh)
        return new_words

if __name__ == '__main__':
    ulu_proc = Processor()
    new_dic = ulu_proc.build_dict()
    pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(new_dic)
    haw_words = Counter(new_dic.keys())
    #pp.pprint(haw_words)
    print(f'Processed {sum((1 for w in haw_words.keys() if w is not None))} '
          f'total words in this run.')




