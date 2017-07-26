# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Tests for TweeterSpeakingClock
###########################################################
#
#  -*- coding: utf-8 -*-

# standard modules

# 3rd-party modules
import pytest

# app modules
from twitter.tweeter_speaking_clock import TweeterSpeakingClock
from twitter.tweeter import Tweeter


class TestTweeterSpeakingClock(object):

    @pytest.mark.parametrize("test_q, expected", [
                             ('ʻO ka hola ʻehia kēia?', True),
                             ("'O ka hola 'ehia keia?", True),
                             ('What time is it?', True),
                             ("What's the time?", True)])
    def test_asks_time(self, test_q, expected):
        t = TweeterSpeakingClock()
        assert t.asks_time(test_q) == expected

