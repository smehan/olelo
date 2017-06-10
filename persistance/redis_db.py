###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Base class for connecting and interacting with Redis DB
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import hashlib

# 3rd-party libs
import redis
from typing import Sequence, TypeVar

# application libs
from grammar import HAW_POS


# Generic Types
T = TypeVar('T')


class RedisDB(object):
    """
    Base class with base connection and methods for interacting with Redis DB
    """

    def __init__(self):
        self.rdb = redis.StrictRedis()
        self.encoding = 'utf-8'

    def destroy(self):
        print("Closing connection to Redis DB....")

    def __str__(self):
        return f'A connection object to a Redis Instance'

    def __repr__(self):
        return f'< RedisDB() - {self.rdb} - {self.encoding} >'

    def encode_s(self, s: str) -> str:
        """
        encode a string: str with the default encoding and return that str
        :param s: s to encode
        :return: encoded string
        """
        return s.encode(self.encoding)

    def decode_s(self, s: str) -> str:
        """
        decode a string: str with the default encoding and return that str.
        :param s: s to decode
        :return: decoded string
        """
        return s.decode()

    def _add_key_to_id_hash(self, name: str, key: str) -> str:
        """
        Given an entry, encode all strings as utf-8 and set a sha1 id
        in a redis hash resulting with entries key:id.
        This is a lookup hash for subsequent data, e.g.
        hash name1:id1 name2:id2 ...
        :param name: name to give to the hash
        :param key: key to add to hash
        :return: redis hash name
        """
        if key is None or key == '':
            return
        hash_entry = {key: hashlib.sha1(self.encode_s(key)).hexdigest()}
        return self._add_keys_to_hash(name,
                                     'id',
                                      hash_entry)

    def _add_keys_to_hash(self, name: str, id: str, *args: T) -> str:
        """
        For a hash given by name:id, adds k, v in args to said hash.
        :param name: str name of hash, e.g. 'defs'
        :param id: str to use as second part of hash_name
        :param args: sequence or mapping to iterate through and add as k, v in hash
        :return: hash_name
        """
        rdb = self.rdb
        if name is None or name == '':
            raise ValueError("Redis hash needs a name....")
        if id is None or id == '':
            return
        hash_name = ':'.join([name, id])
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    rdb.hset(hash_name,
                             self.encode_s(k),
                             self.encode_s(v))
        return hash_name

    def _all_keys_from_hash(self, name: str) -> list:
        """
        Return a list of all keys in a hash
        :param name: 
        :return: 
        """
        rdb = self.rdb
        try:
            return [k.decode() for k, _ in rdb.hgetall(name).items()]
        except:
            return None

    def _all_values_from_hash(self, name: str) -> list:
        """
        Return a list of all values in a hash
        :param name: name of the hash
        :return: list of all values
        """
        rdb = self.rdb
        try:
            return [v.decode() for _, v in rdb.hgetall(name).items()]
        except:
            return None

    def _all_hash(self, name: str) -> dict:
        """
        Return a dict of decoded keys, values in a hash
        :param name: name of the hash
        :return: dict of all k, v
        """
        rdb = self. rdb
        try:
            return {k.decode(): v.decode() for k, v in rdb.hgetall(name).items()}
        except:
            return None

    def _v_from_hash(self, name: str, key: str) -> str:
        """
        Return a hash value for a given key.
        :param name: name of the hash to read
        :param key: hash key to query
        :return: value for the given key
        """
        rdb = self.rdb
        try:
            return rdb.hget(name, self.encode_s(key)).decode()
        except:
            raise ValueError("That name:key doesn't work ...")

    def _add_to_set(self, name: str, hash_id: str, values: Sequence[T]) -> str:
        """
        Given an entry, encode all strings as utf-8 and create
        a redis set with name with values
        :param name: name to join to the set name
        :param hash_id: id to join to the set name
        :param values: sequence of values to encode and and to the set
        :return: redis set name
        """
        rdb = self.rdb
        if name is None or name == '':
            raise ValueError("Redis set needs an id....")
        if hash_id is None or hash_id == '':
            raise ValueError("Redis set needs an id...")
        if values is None or len(values) == 0:
            return
        set_name = self.encode_s(':'.join([name, hash_id]))
        rdb.sadd(set_name, *values)
        return set_name

    def _all_set(self, name:str):
        """
        Given a valid set, return all the decoded members of the set as strings
        with no set order.
        :param name: 
        :return: 
        """
        rdb = self.rdb
        return [e.decode() for e in rdb.smembers(name)]





