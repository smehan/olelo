# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Tests for Tweeter for connecting to twitter
###########################################################
#
#  -*- coding: utf-8 -*-

# standard modules

# 3rd-party modules
import pytest

# app modules
from twitter.tweeter import Tweeter


class TestTweeter(object):

    def setup_class(self):
        print("\nTestTweeter setting up ...\n\n")
        self.t = Tweeter(debug=True)

    @classmethod
    def teardown_class(cls):
        pass

    def test_print_tweets(self):
        assert '#Hawaiian:' in self.t.print_tweets()
