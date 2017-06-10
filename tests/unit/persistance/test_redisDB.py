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
def r():
    """
    create a redis connection object for the test, then cleans up
    after the tests are finished.   
    :return: 
    """
    print("\nMaking a RedisDB instance")
    r = RedisDB()
    yield r
    r.rdb.delete('test_hash:id',
                 'test_map_hash:123',
                 'test_seq_hash:234',
                 'test_set:00942f4668670f34c5943cf52c7ef3139fe2b8d6')


@pytest.fixture(scope='function')
def make_test_id_hash(rdb):
    """
    
    :param rdb: RedisDB connection object
    :return: 
    """
    h = rdb._add_key_to_id_hash('test_hash', 'test_key')
    return h


class TestRedisDB(object):

    def test_encode_s(self, r):
        assert r.encode_s('abc') == b'abc'

    def test_decode_s(self, r):
        assert r.decode_s(b'abc') == 'abc'

    def test__add_key_to_hash(self, r):
        assert r._add_keys_to_hash('test_map_hash', '123', {'1': 'a', '2': 'b'}) == 'test_map_hash:123'
        assert r.rdb.hgetall('test_map_hash:123') == {b'1': b'a', b'2': b'b'}
        assert r._add_keys_to_hash('test_seq_hash', '234', ['a', 'b', 'c']) == 'test_seq_hash:234'
        assert r.rdb.hgetall('test_seq_hash:234') == {b'1': b'a', b'2': b'b', b'3': b'c'}
        with pytest.raises(ValueError):
            r._add_keys_to_hash(None, None)
        assert r._add_keys_to_hash('test_hash', None) == None
        assert r._add_keys_to_hash('test_hash', 'test_key') == 'test_hash:test_key'

    def test__all_keys_from_id_hash(self, r):
        h = make_test_id_hash(r)
        assert r._all_keys_from_hash(h) == ['test_key']

    def test__all_values_from_hash(self, r):
        h = make_test_id_hash(r)
        assert r._all_values_from_hash(h) == ['00942f4668670f34c5943cf52c7ef3139fe2b8d6']

    def test__all_hash(self, r):
        h = make_test_id_hash(r)
        assert r._all_hash(h) == {'test_key': '00942f4668670f34c5943cf52c7ef3139fe2b8d6'}

    def test__v_from_hash(self, r):
        h = make_test_id_hash(r)
        assert r._v_from_hash(h, 'test_key') == '00942f4668670f34c5943cf52c7ef3139fe2b8d6'

    def test__add_to_set(self, r):
        assert r._add_to_set('test_set',
                             '00942f4668670f34c5943cf52c7ef3139fe2b8d6',
                             ['a', 'b', 'c']) == b'test_set:00942f4668670f34c5943cf52c7ef3139fe2b8d6'
        with pytest.raises(ValueError):
            r._add_to_set(None,
                          '00942f4668670f34c5943cf52c7ef3139fe2b8d6',
                          ['a', 'b', 'c'])
            r._add_to_set('',
                          '00942f4668670f34c5943cf52c7ef3139fe2b8d6',
                          ['a', 'b', 'c'])
            r._add_to_set('test_set',
                          '',
                          ['a', 'b', 'c'])
        assert r._add_to_set('test_set',
                             '00942f4668670f34c5943cf52c7ef3139fe2b8d6',
                             []) == None
        assert r._add_to_set('test_set',
                             '00942f4668670f34c5943cf52c7ef3139fe2b8d6',
                             None) == None

    def test__all_set(self, r):
        assert sorted(r._all_set('test_set:00942f4668670f34c5943cf52c7ef3139fe2b8d6')) == ['a', 'b', 'c']

