# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Tests for Processor for transforming proverb source html into usable data
###########################################################
#
#  -*- coding: utf-8 -*-

# standard modules

# 3rd-party modules
import pytest

# app modules
from processor.puk_processor import Processor
from tests.unit.processor.processor_resources import SRC_HTML, SRC_TEXT






"'265    E ao o miki aku o Ka-‘ili-pehu.'"

class TestPukProcessor(object):

    def setup_class(self):
        print(f"\nTestPukProcessor setting up ...\n\n")
        self.p = Processor(path='tests/unit/processor', names='processor_src.html')

    @classmethod
    def teardown_class(cls):
        pass

    def test_get_proverb(self):
        assert self.p.get_proverb(None) == None
        assert self.p.get_proverb("'265    E ao o miki aku o Ka-‘ili-pehu.'") == \
               'E ao o miki aku o Ka-‘ili-pehu.'

