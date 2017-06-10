###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Class that loads in a serialized object and loads it into redis for application usage
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


class RedisLoader(RedisDB):
    """
    Take processed 
    """

    def __init__(self):
        super().__init__()
        self.path = os.path.join('../tmp/', 'new_words.pickle')

    def __repr__(self):
        return f'<RedisLoader()'

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
            hw_ids = self._add_key_to_id_hash('haw', k)
        return hw_ids
        # r = self.rdb
        # results = r.hgetall(hw_ids)
        # for hw, hw_id in results.items():
        #     print(f'{hw.decode()} has id: {hw_id.decode()}')

    def _add_pos(self, hw_id):
        pass

    def _add_parts(self, d, id_hash):
        """
        Takes dictionary and adds parts for each entry
        :param d: dict from processed input
        :param id_hash: This is the hash of ids for hawaiian hw
        :return: 
        """
        all_ids = self._all_hash(id_hash).keys()
        for hw, v in d.items():
            if hw is None:
                continue
            if hw in all_ids:
                hw_id = self._v_from_hash(id_hash, hw)
                _ = self._add_to_set('pos', hw_id, d[hw]['pos'])
                _ = self._add_to_set('content', hw_id, d[hw]['content'])
                _ = self._add_key_to_hash('defs', hw_id, d[hw]['defs'])

    def load_redis(self):
        haw_words = self._get_data()
        hw_ids = self._make_hw_hash(haw_words)
        self._add_parts(haw_words, hw_ids)


if __name__ == '__main__':
    haw_loader = RedisLoader()
    haw_loader.load_redis()