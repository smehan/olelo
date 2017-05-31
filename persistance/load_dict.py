###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Class that loads in a serialized object and loads it into redis for application usage
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os
import copy
from collections import Counter
import pickle
import hashlib

# 3rd-party libs
import redis

# application libs
from redis_db import RedisDB
from grammar import HAW_POS


class RedisLoader(RedisDB):
    """
    Take processed 
    """

    def __init__(self):
        super().__init__()
        self.path = os.path.join('../tmp/', 'new_words.pickle')

    def _get_data(self):
        with open(self.path, 'rb') as fh:
            return pickle.load(fh)

    def _make_hw_hash(self, d):
        """
        Takes dictionary and makes a headword:id :HASH
        :param d: dict from processed input
        :return: 
        """
        for k, v in d.items():
            if k is None:
                continue
            print(k, v)
            hw_ids = self._make_hash('haw', k)
        r = self.rdb
        results = r.hgetall(hw_ids)
        for hw, hw_id in results.items():
            print(f'{hw.decode()} has id: {hw_id.decode()}')

    def load_redis(self):
        haw_words = self._get_data()
        self._make_hw_hash(haw_words)


if __name__ == '__main__':
    haw_loader = RedisLoader()
    haw_loader.load_redis()