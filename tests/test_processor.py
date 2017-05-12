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
from .processor_resources import SRC_HTML, SRC_TEXT

# def test_get_src():
#     p = Processor()
#     assert p.get_src()


@pytest.fixture(scope='class')
def p():
    return Processor(path='tests/', names='processor_src.html')


@pytest.fixture(scope='class')
def src_html() -> str:
    return SRC_HTML


@pytest.fixture(scope='class')
def src_text():
    return SRC_TEXT


class TestProcessor(object):

    @classmethod
    def setup_class(cls):
        print("\nThis is the setup in the class...\n\n")

    @classmethod
    def teardown_class(cls):
        pass

    def test_get_src(self, p):
        assert p.get_src().text == src_text()

    def test_get_dict_entries(self, p):
        with pytest.raises(TypeError):
            p.get_dict_entries(1)
            p.get_dict_entries('some text')

    def test_parse_content(self):
        pass

    def test_build_entry(self):
        pass

