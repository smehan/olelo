###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
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
from grammar import HAW_POS


class RedisSearch(RedisDB):
    """

    """

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f'<RedisSearch()'

    def find_hw(self, huid):
        """
        Given a valid HUID, will return the hawaiian hw
        that is paired with that HUID as well as
        definitions and pos.
        :param huid:
        :return:
        """
        hw_hash = self._all_hash('haw:id')
        for k, v in hw_hash.items():
            if v == huid:
                word_defs = self._all_values_from_hash(':'.join(['defs', huid]))
                word_pos = self.rdb.smembers(':'.join(['pos', huid]))
                print(f'HW - {k}, HUID - {v}')
                print(f'Defs - {word_defs}')
                print(f'POS - {word_pos}')


if __name__ == '__main__':
    haw_searcher = RedisSearch()
    haw_searcher.find_hw('e2323d46da844920ba5d2e6da1d72b0fc76f09d8')
