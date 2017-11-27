###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Class to instantiate a twitter interface to communicate with twitter
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os
import logging
import datetime as dt
import pytz

# 3rd-party libs
import tweepy
import yaml

# application libs
import loggerUtils as lg


class Tweeter(object):
    def __init__(self, debug=True, **kwargs):
        super().__init__(**kwargs)

        lg.loggerutils.init_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Olelo twitter started and logging enabled")

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "local.cfg"), "r") as fh:
            cfg = yaml.load(fh)

        self.screen_name = cfg['screen_name']
        auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
        auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
        self.API = tweepy.API(auth)

        self.DEBUG = debug

    def __repr__(self):
        return f'< {self.__class__.__name__} using screen {self.screen_name} >'

    def print_tweets(self):
        api = self.API
        data = api.user_timeline(screen_name=self.screen_name, count=100, include_rts=True)
        for d in data:
            return d._json['text']

    def tweeted_today(self):
        """Checks if a tweet was posted today"""
        api = self.API
        last_tweet = api.user_timeline(screen_name=self.screen_name, count=1, include_rts=False)
        if last_tweet[0].created_at.date() == dt.date.today():
            return True
        return False

    @staticmethod
    def twitter_now() -> dt.datetime:
        return dt.datetime.now(tz=pytz.utc)

    @staticmethod
    def twitter_time(twitter_time: dt.datetime) -> dt.datetime:
        """
        returns a localized dt object corresponding to the twitter UTC tz
        :param twitter_time:
        :return:
        """
        return twitter_time.replace(tzinfo=pytz.utc)


if __name__ == "__main__":
    t = Tweeter(debug=True)
    t.logger.info(t.print_tweets())