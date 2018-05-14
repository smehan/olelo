# Copyright (C) 2018 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Tests for Grammar class for language related methods
###########################################################
#
#  -*- coding: utf-8 -*-

# standard modules

# 3rd-party modules
import pytest

# app modules
from grammar import standardize_okina


def test_standardize_okina():
    assert standardize_okina('test') == 'test'
    assert standardize_okina("‘") == 'ʻ'  # U2018 vs U02BB
    assert standardize_okina('ʻono') == 'ʻono'  #U02BB vs U02BB
    assert standardize_okina("'ono") == 'ʻono'  # APOSTROPHE U0027 vs U02BB
    assert standardize_okina("‘ono") == 'ʻono'  # U2018 vs U02BB
    assert standardize_okina("ʻ'‘") == "ʻʻʻ"  # All vs U02BB

