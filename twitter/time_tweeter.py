###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Class to instantiate a twitter stream listener to listen for requests for
# what time is it.
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os
import time

# 3rd-party libs
import tweepy
import yaml

# application libs
from persistance.redis_db import RedisDB
import translations.time_as_words as taw


class StreamListener(tweepy.StreamListener):

    def __init__(self, debug=True):
        super().__init__()

        #init_logging()
        #self.logger = logging.getLogger(__name__)
        #self.logger.info("Job started and logging enabled")

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "local.cfg"), "r") as fh:
            cfg = yaml.load(fh)

        self.screen_name = cfg['screen_name']
        auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
        auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
        self.API = tweepy.API(auth)
        #self.STREAM = tweepy.Stream(auth, self)

        self.DEBUG = debug

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def print_tweets(self):
        api = self.API
        data = api.mentions_timeline(count=100)
        for d in data:
            print(d._json['text'])

    def build_time(self):
        ts = taw.time_to_words("now")
        return f"E pal, " + ts

    def speaking_clock(self):
        clock_is_on = True
        while clock_is_on:
            print("Checking for times...")
            self.print_tweets()
            print(self.build_time())
            time.sleep(250)

if __name__ == '__main__':
    t = StreamListener()
    t.speaking_clock()
    #stream_listener = StreamListener()
    stream = tweepy.Stream(auth=t.API.auth, listener=t)
    #stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    #stream.filter(track=["KaKa_Olelo", "hawaiianclock, HawaiianClock, HawaiianClock"])
    stream.userstream(replies=all)