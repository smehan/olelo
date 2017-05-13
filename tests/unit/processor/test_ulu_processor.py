# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Tests for Processor for transforming source html into usable data
###########################################################
#
#  -*- coding: utf-8 -*-

# standard modules

# 3rd-party modules
import pytest

# app modules
from processor.ulu_processor import Processor
from tests.unit.processor.processor_resources import SRC_HTML, SRC_TEXT


# def test_get_src():
#     p = Processor()
#     assert p.get_src()


@pytest.fixture(scope='class')
def src_html() -> str:
    return SRC_HTML


@pytest.fixture(scope='class')
def src_text():
    return SRC_TEXT


class TestProcessor(object):

    def setup_class(self):
        print("\nThis is the setup in the class...\n\n")
        self.p = Processor(path='tests/unit/processor', names='processor_src.html')

    @classmethod
    def teardown_class(cls):
        pass

    def test_get_src(self):
        assert self.p.get_src().text == src_text()

    def test_get_dict_entries(self):
        with pytest.raises(TypeError):
            self.p.get_dict_entries(1)
            self.p.get_dict_entries('some text')

    def test_parse_content(self):
        assert self.p.parse_content('') == (None, None)
        assert self.p.parse_content(None) == (None, None)
        assert self.p.parse_content('''a 
1. prep. Of, acquired by. This a forms part of the possessives, as in ka'u, mine, and kāna, his. (Gram. 9.6.1.)ʻUmi-a-Līloa, ʻUmi, [son] of Līloa. Hale-a-ka-lā, house acquired [or used] by the sun [mountain name]. (PPN ʻa.)
2. (Cap.) nvs. Abbreviation of ʻākau, north, as in surveying reports.
''') == ('a', ["1. prep. Of, acquired by. This a forms part of the possessives, as in ka'u, mine, and kāna, his. (Gram. 9.6.1.)ʻUmi-a-Līloa, ʻUmi, [son] of Līloa. Hale-a-ka-lā, house acquired [or used] by the sun [mountain name]. (PPN ʻa.)", '2. (Cap.) nvs. Abbreviation of ʻākau, north, as in surveying reports.'])

    def test_build_entry(self):
        pass


