# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Tests for Processor for transforming source html into usable data
###########################################################
#
#  -*- coding: utf-8 -*-

# standard modules
from unittest import TestCase

# 3rd-party modules
import pytest

# app modules
from processor.ulu_processor import Processor

# def test_get_src():
#     p = Processor()
#     assert p.get_src()


class TestProcessor(object):

    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    def test_get_dict_entries(self):
        p = Processor()
        with pytest.raises(TypeError):
            p.get_dict_entries(1)
            p.get_dict_entries('some text')

    def test_parse_content(self):
        pass

    def test_build_entry(self):
        pass
