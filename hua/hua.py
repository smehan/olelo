###########################################################
# Copyright (C) 2018 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Class to drive redis interface for dictionary words
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
from itertools import chain

# 3rd-party libs

# application libs
from persistance.redis_db import RedisDB


class Hua(RedisDB):
    def __init__(self, **kwargs):
        super().__init__()

    @staticmethod
    def _clean_line(s: str)-> str:
        """Remove unneeded characters from string"""
        UNNEEDED_CHARS = ['[', ']', "'"]
        ALT_TEXT = {'Cf.': 'See also',
                    'Lit.': 'Literally'}
        for c in UNNEEDED_CHARS:
            s.replace(c, '')
        for k, v in ALT_TEXT.items():
            s.replace(k, v)
        return s

    def form_def(self, defs)-> str:
        """Form a str to use as the tweet def"""
        if isinstance(defs, str):
            new_defs = self._clean_line(defs)
        elif isinstance(defs, list):
            new_list = []
            for e in defs:
                new_list.append(self._clean_line(e))
            new_defs = " ".join(new_list)
        return new_defs

    def get_word(self, huid=None):
        """
        retrieve definition and POS for a given huid. If no huid given,
        will select a random key.
        :param huid:
        :return:
        """
        if not huid:
            huid = self._get_random_key()
        hw_hash = self._all_hash('haw:id')
        for k, v in iter(hw_hash.items()):
            if v == huid:
                word_defs = self._all_values_from_hash(':'.join(['defs', huid]))
                word_pos = self.rdb.smembers(':'.join(['pos', huid]))
                print(f'{k} {word_defs}: {word_pos}')
                return f'{k} {word_defs}: {word_pos}'

    def make_word_of_day(self):
        """retrieve a random word of the day with defs and pos"""
        return self.get_word()


if __name__ == "__main__":
    words = Hua(debug=True)
    words.make_word_of_day()
