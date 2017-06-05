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


@pytest.fixture(scope='class')
def src_html() -> str:
    return SRC_HTML


@pytest.fixture(scope='class')
def src_text():
    return SRC_TEXT


class TestProcessor(object):

    def setup_class(self):
        print("\nTestProcessor setting up ...\n\n")
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
2. (Cap.) nvs. Abbreviation of ʻākau, north, as in surveying reports.''') == \
               ('a', ["1. prep. Of, acquired by. This a forms part of the possessives, as in ka'u, mine, and kāna, his. (Gram. 9.6.1.)ʻUmi-a-Līloa, ʻUmi, [son] of Līloa. Hale-a-ka-lā, house acquired [or used] by the sun [mountain name]. (PPN ʻa.)",
               '2. (Cap.) nvs. Abbreviation of ʻākau, north, as in surveying reports.'])
    # TODO somewhere this is getting output as multiple strings in a list in content
    """
        'ʻāwaʻa': {   'content': [   'nvt. Long, narrow excavation, trench, ditch, '
                                 'gully; to dig a ditch or furrow.'],
                  'id': 'A.1671',
                  'pos': ['noun', 'transitive verb']},
                  
          'ʻāpā': {   'content': [   'n.',
                   '1. Roll or ream, as of paper; bolt, as of '
                   'cloth.',
                   '2. See lima ʻāpā.'],
    """

    def test_build_entry(self):
        """,
              ["1. prep. Of, acquired by. This <HAW>a</HAW> forms part of the possessives, as in <HAW>ka'u</HAW>, mine, and <HAW>kāna</HAW>, his. (Gram. 9.6.1.)<HAW>ʻUmi-a-Līloa</HAW>, <HAW>ʻUmi</HAW>, [son] of <HAW>Līloa</HAW>. <HAW>Hale-a-ka-lā</HAW>, house acquired [or used] by the sun [mountain name]. (PPN <HAW>ʻa</HAW>.)",
               '2. (Cap.) nvs. Abbreviation of <HAW>ʻākau</HAW>, north, as in surveying reports.']
        """
        page = self.p.get_src()
        refs = self.p.get_dict_entries(page)
        for r in refs:
            """
            {'a': {'content': ["1. prep. Of, acquired by. This a forms part of the possessives, as in ka'u, mine, and kāna, his. (Gram. 9.6.1.)ʻUmi-a-Līloa, ʻUmi, [son] of Līloa. Hale-a-ka-lā, house acquired [or used] by the sun [mountain name]. (PPN ʻa.)", 
                               '2. (Cap.) nvs. Abbreviation of ʻākau, north, as in surveying reports.'], 
                   'id': 'A.1'}}
            """
            if r.get('id') == 'A.1':
                print('testing new test')
                test_1 = r
        assert self.p.build_entry(test_1) == {'a': {'content': ["1. prep. Of, acquired by. This a forms part of the possessives, as in ka'u, mine, and kāna, his. (Gram. 9.6.1.)ʻUmi-a-Līloa, ʻUmi, [son] of Līloa. Hale-a-ka-lā, house acquired [or used] by the sun [mountain name]. (PPN ʻa.)",
                                                                '2. (Cap.) nvs. Abbreviation of ʻākau, north, as in surveying reports.'],
                                                    'marked_content_haw': ["1. prep. Of, acquired by. This <HAW>a</HAW> forms part of the possessives, as in <HAW>ka'u</HAW>, mine, and <HAW>kāna</HAW>, his. (Gram. 9.6.1.)<HAW>ʻUmi-a-Līloa</HAW>, <HAW>ʻUmi</HAW>, [son] of <HAW>Līloa</HAW>. <HAW>Hale-a-ka-lā</HAW>, house acquired [or used] by the sun [mountain name]. (PPN <HAW>ʻa</HAW>.)",
                                                                           '2. (Cap.) nvs. Abbreviation of <HAW>ʻākau</HAW>, north, as in surveying reports.'],
                                                    'id': 'A.1'}}


        #assert self.p.build_entry(r) == {'apo pāpale', {'content': ['n. Hatband.'], 'id': 'A.1456'}}
        # words = (self.build_entry(r) for r in refs)
        # assert self.p.build_entry({'apo pāpale': {'content': ['n. Hatband.'], 'id': 'A.1456'}}) == \
        #        ('apo pāpale', {'content': ['n. Hatband.'], 'id': 'A.1456', 'pos': ['noun']})

    def test_get_pos(self):
        assert self.p.get_pos(None) == None

    def test_build_pos(self):
        assert self.p.build_pos(None) == None
        # {'apo pāpale': {'content': ['n. Hatband.'], 'id': 'A.1456'}}
        assert self.p.build_pos(['n. Hatband.']) == ['noun']
        assert self.p.build_pos(['n. Hatband.']) != ['stative verb']
        assert self.p.build_pos(['n. Hatband.']) != ['noun', 'stative verb']
        # {'ʻāʻīʻoʻoleʻa': {'content': ['nvs. Stiff neck. Fig., disobedience, obstinacy; obstinate.'], 'id': 'A.514'}}
        assert self.p.build_pos(['nvs. Stiff neck. Fig., disobedience, obstinacy; obstinate.']) == \
                                ['noun', 'stative verb']
        assert self.p.build_pos(['n.', '1. Roll or ream, as of paper; bolt, as of cloth.',  '2. See lima ʻāpā.']) == \
                                ['noun']
        # TODO Plural

    def test_build_parts(self):
        assert self.p.build_parts(None) == (None, None)
        # {'apo pāpale': {'content': ['n. Hatband.'], 'id': 'A.1456'}}
        assert self.p.build_parts({'apo pāpale': {'content': ['n. Hatband.'], 'id': 'A.1456'}}) == \
               ('apo pāpale', {'content': ['n. Hatband.'], 'id': 'A.1456', 'pos': ['noun']})
        assert self.p.build_parts({'apo pāpale': {'content': ['n. Hatband.'], 'id': 'A.1456'}}) != \
               ('apo pāpale', {'content': ['n. Hatband.'], 'id': 'A.1456', 'pos': ['stative verb']})
        assert self.p.build_parts({'apo pāpale': {'content': ['n. Hatband.'], 'id': 'A.1456'}}) != \
               ('apo pāpale', {'content': ['n. Hatband.'], 'id': 'A.1456', 'pos': ['noun', 'stative verb']})
        # {'ʻāʻīʻoʻoleʻa': {'content': ['nvs. Stiff neck. Fig., disobedience, obstinacy; obstinate.'], 'id': 'A.514'}}
        assert self.p.build_parts({'ʻāʻīʻoʻoleʻa': {'content': ['nvs. Stiff neck. Fig., disobedience, obstinacy; obstinate.'], 'id': 'A.514'}}) == \
               ('ʻāʻīʻoʻoleʻa', {'content': ['nvs. Stiff neck. Fig., disobedience, obstinacy; obstinate.'], 'id': 'A.514', 'pos': ['noun', 'stative verb']})
        assert self.p.build_parts({'ʻāpā': {'content': ['n.', '1. Roll or ream, as of paper; bolt, as of cloth.',  '2. See lima ʻāpā.'],
                                          'id': 'A.1370', 'pos': ['noun']}}) == \
               ('ʻāpā', {'content': ['n.', '1. Roll or ream, as of paper; bolt, as of cloth.',  '2. See lima ʻāpā.'],
                         'id': 'A.1370',
                         'pos': ['noun']})
        # TODO Plural