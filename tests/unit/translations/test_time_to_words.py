# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Tests for time to words class
###########################################################
#
#  -*- coding: utf-8 -*-

# standard modules
import datetime as dt

# 3rd-party modules
import pytest

# app modules
from translations.time_as_words import time_to_words, parse_time, form_words


def t():
    """
    create an instance for local tests
    :return:
    """
    print("\nMaking a TimeToWords instance...")


class TestTimeToWords(object):

    def test_time_to_words_error(self):
        with pytest.raises(ValueError):
            time_to_words("What time is it?")

    def test_time_to_words(self):
        assert time_to_words("12:00") == "ʻO ka hola ʻumikūmālua kēia o ke awakea."
        # assert time_to_words("12:00") == "ʻO ka hola ʻumikūmā o ka ʻauwe."

    def test_parse_time(self):
        assert parse_time("now") == parse_time(dt.datetime.now().strftime("%H:%M"))
        assert parse_time("01:00") == (1, 00)
        assert parse_time("23:59") == (23, 59)

    def test_parse_time_error(self):
        with pytest.raises(AttributeError):
            assert parse_time("1:15")
            assert parse_time("1230")

    def test_form_words(self):
        assert form_words(12, 00) == "ʻO ka hola ʻumikūmālua kēia o ke awakea."
        assert form_words(12, 16) == "ʻO ka hapalua hola ʻumikūmālua kēia o ke awakea."
        assert form_words(12, 50) == "ʻO ka hola ʻumikūmākolu kēia o ke awakea."
