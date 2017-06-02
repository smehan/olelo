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
    print("Making a RedisDB instance")
    r = RedisDB()
    return r


@pytest.mark.usefixtures('red')
class TestRedisDB(object):

    def test_encode_s(self):
        r = red()
        assert r.encode_s('abc') == b'abc'

    def test_decode_s(self):
        r = red()
        assert r.decode_s(b'abc') == 'abc'

    def test__add_key_to_hash(self):
        self.fail()

    def test__all_keys_from_hash(self):
        self.fail()

    def test__all_values_from_hash(self):
        self.fail()

    def test__all_hash(self):
        self.fail()

    def test__v_from_hash(self):
        self.fail()

    def test__add_to_set(self):
        self.fail()
