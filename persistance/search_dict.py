###########################################################
# Copyright (C) 2018 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Class that searches in a redis for exploration
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os
import pickle

# 3rd-party libs

# application libs
from redis_db import RedisDB
from processor.grammar import HAW_POS


class RedisSearch(RedisDB):
    """

    """

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f'<RedisSearch()'

    def find_hw(self, huid=None, hw=None):
        """
        Given a valid HUID or Hawaiian headword,
        will print the hawaiian hw
        that is paired with that HUID as well as
        definitions and pos.
        :param huid: HUID token
        :param hw: HAW headword string
        :return:
        """
        hw_hash = self._all_hash('haw:id')
        for k, v in hw_hash.items():
            if (huid and v == huid) or (hw and k == hw):
                word_defs = self._all_values_from_hash(':'.join(['defs', v]))
                word_pos = self.rdb.smembers(':'.join(['pos', v]))
                print(f'HW - {k}, HUID - {v}')
                print(f'Defs - {word_defs}')
                print(f'POS - {word_pos}')


if __name__ == '__main__':
    haw_searcher = RedisSearch()
    haw_searcher.find_hw(huid='5bb6fffeffef6622eafe0e99c410b2fc9bf50cc5')
    haw_searcher.find_hw(hw='ālaala')