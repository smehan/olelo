###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Class to instantiate a twitter interface to communicate with twitter
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os

# 3rd-party libs
import tweepy
import yaml

# application libs


class Tweeter(object):
    def __init__(self, debug=True):
        #init_logging()
        #self.logger = logging.getLogger(__name__)
        #self.logger.info("Job started and logging enabled")

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "local.cfg"), "r") as fh:
            cfg = yaml.load(fh)

        self.screen_name = cfg['screen_name']
        auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
        auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
        self.API = tweepy.API(auth)

        self.DEBUG = debug

    def print_tweets(self):
        api = self.API
        data = api.user_timeline(screen_name=self.screen_name, count=100, include_rts=True)
        for d in data:
            return d._json['text']

    def push_tweet(self):
        api = self.API
        tweet = "#Hawaiian Word Of The Day: " + 'dummy text'
        if self.DEBUG:
            print(f'About to tweet: {tweet}')
        else:
            status = api.update_status(status=tweet)


if __name__ == "__main__":
    t = Tweeter(debug=True)
    print(t.print_tweets())
    t.push_tweet()
