###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Base class for connecting and interacting with Redis DB
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os
import hashlib

# 3rd-party libs
import redis

# application libs
from grammar import HAW_POS


class RedisDB(object):
    """
    Base class with base connection and methods for interacting with Redis DB
    """

    def __init__(self):
        self.rdb = redis.StrictRedis()

    def destroy(self):
        print("Closing connection to Redis DB....")

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def _make_hash(self, name: str, key: str):
        """
        Given a dict entry, encode all strings as utf-8 and set a sha1 id
        in a redis hash with name
        :param name: name to give to the hash
        :return: redis hash name
        """
        rdb = self.rdb
        if name is None or name == '':
            raise ValueError("Hash needs a name....")
        if key is None or key == '':
            return
        encoded_key = key.encode('utf-8')
        hash_name = ':'.join([name, 'id'])
        rdb.hset(hash_name,
                 encoded_key,
                 hashlib.sha1(encoded_key).hexdigest())
        return hash_name

