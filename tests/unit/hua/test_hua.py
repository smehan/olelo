# Copyright (C) 2018 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Tests for Hua class of dictionary type methods
###########################################################
#
#  -*- coding: utf-8 -*-

# standard modules

# 3rd-party modules
import pytest

# app modules
from hua.hua import Hua
from tests.unit.processor.processor_resources import SRC_HTML, SRC_TEXT


class TestHua(object):

    def setup_class(self):
        print(f'Setting up a Test Hua ...\n\n')
        self.hua = Hua()

    def teardown_class(self):
        pass

    def test_hua(self):
        assert self.hua

    def test_get_word(self):
        pass

    def test_make_word_of_day(self):
        assert isinstance(self.hua.make_word_of_day(), str)