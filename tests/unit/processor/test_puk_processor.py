# Copyright (C) 2019 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Tests for Processor for transforming proverb source html into usable data
###########################################################
#
#  -*- coding: utf-8 -*-

# standard modules
import os
from collections import defaultdict

# 3rd-party modules
import pytest

# app modules
from processor.puk_processor import Processor


"'265    E ao o miki aku o Ka-‘ili-pehu.'"


class TestPukProcessor(object):

    def setup_class(self):
        print(f"\nTestPukProcessor setting up ...\n\n")
        self.path = 'unit/processor'
        self.name = 'proverbs_src.html'
        self.fn = os.path.join(self.path, self.name)
        self.p = Processor(self.path, self.name)

    @classmethod
    def teardown_class(cls):
        pass

    def test_get_src(self):
        pass

    def test_get_puk_entries(self):
        assert len(self.p.get_puk_entries(self.p.get_src(self.fn))) == 9

    def test_parse_content(self):
        pass

    def test_prepare_source(self):
        pass

    def test_get_body(self):
        pass

    def test_split_entries(self):
        entries_list = self.p.get_puk_entries(self.p.get_src(self.fn))
        assert isinstance(self.p.split_entries(entries_list), defaultdict)

    def test_get_proverb(self):
        assert self.p.get_proverb(None) == None
        assert self.p.get_proverb("'265    E ao o miki aku o Ka-‘ili-pehu.'") == \
                                  'E ao o miki aku o Ka-‘ili-pehu.'

    def test_build_source_entry(self):
        pass

    def test_build_proverbs(self):
        assert self.p.build_proverbs() == {'Hi': 'There'}

