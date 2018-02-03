###########################################################
# Copyright (C) 2018 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Processor for transforming dictionary source html into usable data
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


class Processor(object):
    """
    This class reads in the html source of the dict and transforms it into usable string: encoded data.
    """
    ULUDICTSRCPATH = '../ulu-dict/'
    ULUDICTSRCFILES = 'puk-*.html'
    TMPPATH = '../tmp/'

    # Regex patterns compiled here for speed
    CONTENT_POS = re.compile(r'^(?:\d+\.\s)?[a-z.]+\.')
    CONTENT_DEF = re.compile(r'^(?:\d+\.\s)?(.*)$')

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

    def get_pos(self, s: str) -> list:
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
            # TODO A.3 shows 'conj. and prep.'
        except AttributeError:
            return all_pos
        for pos, abbrevs in HAW_POS.items():
            for e in abbrevs:
                if e in s and pos not in all_pos:
                    all_pos.append(pos)
        # if there is no result for pos, mark it unknown
        if len(all_pos) == 0:
            all_pos.append('UNKNOWN')
        return all_pos

    def build_pos(self, contents: list) -> list:
        """
        Parse an entry and return all Parts-of-speech.
        :param contents: list
        :return: list ['noun', 'verb', ...]
        """
        if contents is None:
            return None
        all_lines = set([pos for item in contents for pos in self.get_pos(item) if len(self.get_pos(item)) > 0])
        return sorted(list(all_lines))

    def get_def(self, s: str) -> str:
        """
        Parse a contents string and extract the definition text.
        First splits on a match with pos regex.
        If no match, then pulls the definition contents.
        :param s: an element of contents in source_dict
        :return:
        """
        if s is None:
            return None
        try:
            parts = re.split(self.CONTENT_POS, s)
        except TypeError:
            raise TypeError(f'Problem splitting on {s}')
        # got a good string after splitting on pos
        if len(parts) > 1 and parts[1] != '':
            return parts[1].strip()
        # Now two cases. 1. There was a single word in line, e.g. '3. Croup'    .
        if len(self.get_pos(s)) == 0:
            return re.match(self.CONTENT_DEF, s).group(1)
        # only a pos in the line
        return None

    def build_defs(self, contents: list, existing_defs: dict = None) -> dict:
        """
        Parse an entry and return all definitions added as a sub-dict.
        If there are existing defs, append the new defs.
        :param contents: list
        :param existing_defs: dict of existing defs
        :return: dict {'defs': {'1': 'text here', ...}
        """
        if contents is None or len(contents) == 0:
            return None
        if existing_defs is not None:
            def_dict = existing_defs
        else:
            def_dict = {}
        def_count = len(def_dict)
        for i, _ in enumerate(contents):
            s = self.get_def(contents[i])
            if s is not None:
                def_count += 1
                def_dict[def_count] = s
        return def_dict

    def build_parts(self, entry: dict) -> dict:
        """
        For each source entry, build out components of parsed dictionary entry,
        including pos, definitions,
        body is a dict containing all components.
        :param entry:
        :return: tuple (hw, body)
        """
        if entry is None:
            return None, None
        (hw, body), = entry.items()
        body['pos'] = self.build_pos(body['content'])
        body['defs'] = self.build_defs(body['content'])
        return hw, body

    def make_entry(self, d: dict, entry: tuple) -> dict:
        """
        Take an entry (hw, body) and either return it as a new
        key in the master dict or return as an existing entry
        with an updated body
        :param d: master dict
        :param entry: tuple (hw, entry_body)
        :return: {hw: body}
        """
        hw, body = entry[0], entry[1]
        if hw in d:
            d[hw]['id'].extend(body['id'])
            d[hw]['content'].extend(body['content'])
            #d[hw]['marked_content_haw'].extend(body['marked_content_haw'])
            d[hw]['defs'].update(self.build_defs(body['content'], d[hw]['defs']))
            d[hw]['pos'] = list(set(d[hw]['pos'] + body['pos']))
            return {hw: d[hw]}

        return {hw: body}

    def make_dict(self, source_dict: dict) -> dict:
        """
        Take the parsed entries from html source and 
        form a master dict with appropriate attrs.
        :param source_dict: 
        :return: new_dict with all parts formed.
        """
        new_dict = {}
        for entry in source_dict:
            hw, rest = self.build_parts(entry)
            if hw is None:
                continue
            new_dict.update(self.make_entry(new_dict, (hw, rest)))
        return new_dict

    def build_dict(self) -> dict:
        """
        reads in source html and outputs a dict with all entries.
        Includes a serialized object on disk.
        :return: 
        """
        new_words = {}
        for name in glob.glob(os.path.join(self.srcpath, self.fname)):
            print(name)
            source_words = self.prepare_source(fn=name)
            new_words.update(self.make_dict(source_words))
        with open(os.path.join(self.TMPPATH, 'new_words.pickle'), 'wb') as fh:
            pickle.dump(new_words, fh)
        return new_words


if __name__ == '__main__':
    ulu_proc = Processor()
    new_dic = ulu_proc.build_dict()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(new_dic)

    # frequencies
    haw_word_freqs = Counter(new_dic.keys())
    #pp.pprint(haw_word_freqs)
    #print(f'Processed {sum((1 for w in haw_word_freqs.keys() if w is not None))} '
    #      f'total head words in this run.')

    # This checks the list of words processed and finds missing entries
    id_list = []
    for w in new_dic:
        for e in new_dic[w].get('id'):
            id_list.append(e)

    for i in range(1, 1762):
        if '.'.join(['A', str(i)]) not in id_list:
            print(f"Whoa, no A.{i}!")




