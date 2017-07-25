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
from collections import deque

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
        self.last_reqs = deque(maxlen=100)
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

    def asks_time(self, body):
            if 'ʻO ka hola ʻehia kēia?' in body:
                return True
            return False

    def build_time(self, name):
        ts = taw.time_to_words("now")
        return f"E @{name}, " + ts

    def post_time_reply(self, status_id, body):
        api = self.API
        if self.DEBUG:
            print(f"{status_id} gets the tweet: {body}")
        else:
            api.update_status(status=body,
                              in_reply_to_status_id_str=status_id)

    def build_link(self, screen_name, tweet_id):
        return f"https://twitter.com/{screen_name}/status/{tweet_id}"

    def post_time_retweet(self, reply_to, user):
        api = self.API
        body = f"{self.build_time(user._json['screen_name'])} {self.build_link(user._json['screen_name'], reply_to._json['id_str'])}"
        if self.DEBUG:
            print(body)
        else:
            api.update_status(status=body,
                              in_reply_to_status_id_str=reply_to._json['id_str'])

    def check_tweets(self):
        api = self.API
        recent_tweets = api.mentions_timeline(count=100)
        for rt in recent_tweets:
            if rt._json['id_str'] in self.last_reqs:
                continue
            self.last_reqs.appendleft(rt._json['id_str'])
            if self.asks_time(rt._json['text']):
                user = api.get_user(user_id=rt._json['user']['id'])
                self.post_time_reply(status_id=rt._json['id_str'],
                                     body=self.build_time(user._json['screen_name']))
                self.post_time_retweet(reply_to=rt,
                                       user=user)

    def speaking_clock(self):
        clock_is_on = True
        while clock_is_on:
            print("Checking for times...")
            self.check_tweets()
            time.sleep(250)

if __name__ == '__main__':
    t = StreamListener(debug=False)
    t.speaking_clock()
    #stream_listener = StreamListener()
    stream = tweepy.Stream(auth=t.API.auth, listener=t)
    #stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    #stream.filter(track=["KaKa_Olelo", "hawaiianclock, HawaiianClock, HawaiianClock"])
    stream.userstream(replies=all)