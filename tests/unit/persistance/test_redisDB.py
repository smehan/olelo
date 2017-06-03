# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Tests for RedisDB for accessing/setting db entries
###########################################################
#
#  -*- coding: utf-8 -*-

# standard modules

# 3rd-party modules
import pytest

# app modules
from persistance.redis_db import RedisDB


@pytest.fixture(scope='class')
def red():
    """
    create a redis connection object
    :return: 
    """
    print("\nMaking a RedisDB instance")
    r = RedisDB()
    return r

@pytest.fixture(scope='function')
def make_test_hash(rdb):
    """
    
    :param rdb: RedisDB connection object
    :return: 
    """
    h = rdb._add_key_to_hash('test_hash', 'test_key')
    return h



@pytest.mark.usefixtures('red')
class TestRedisDB(object):

    def test_encode_s(self):
        r = red()
        assert r.encode_s('abc') == b'abc'

    def test_decode_s(self):
        r = red()
        assert r.decode_s(b'abc') == 'abc'

    def test__add_key_to_hash(self):
        r = red()
        with pytest.raises(ValueError):
            r._add_key_to_hash(None, None)
        assert r._add_key_to_hash('test_hash', None) == None
        assert r._add_key_to_hash('test_hash', 'test_key') == 'test_hash:id'

    def test__all_keys_from_hash(self):
        r = red()
        h = make_test_hash(r)
        assert r._all_keys_from_hash(h) == ['test_key']

    def test__all_values_from_hash(self):
        r = red()
        h = make_test_hash(r)
        assert r._all_values_from_hash(h) == ['00942f4668670f34c5943cf52c7ef3139fe2b8d6']

    def test__all_hash(self):
        r = red()
        h = make_test_hash(r)
        assert r._all_hash(h) == {'test_key': '00942f4668670f34c5943cf52c7ef3139fe2b8d6'}

    def test__v_from_hash(self):
        r = red()
        h = make_test_hash(r)
        assert r._v_from_hash(h, 'test_key') == '00942f4668670f34c5943cf52c7ef3139fe2b8d6'

    def test__add_to_set(self):
        r = red()
        assert r._add_to_set('test_set',
                             '00942f4668670f34c5943cf52c7ef3139fe2b8d6',
                             ['a', 'b', 'c']) == b'test_set:00942f4668670f34c5943cf52c7ef3139fe2b8d6'

