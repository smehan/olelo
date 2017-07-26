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
import pickle

# 3rd-party libs
import tweepy
import yaml

# application libs
from persistance.redis_db import RedisDB
import translations.time_as_words as taw


class TweeterSpeakingClock(object):

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
        if os.path.isfile('../tmp/last_reqs.pickle'):
            with open(os.path.join('../tmp', 'last_reqs.pickle'), 'rb') as fh:
                self.last_reqs = pickle.load(fh)
        else:
            open(os.path.join('../tmp', 'last_reqs.pickle'), 'w').close()
            self.last_reqs = deque(maxlen=100)

        self.DEBUG = debug

    def print_tweets(self):
        api = self.API
        data = api.mentions_timeline(count=100)
        for d in data:
            print(d._json['text'])

    @staticmethod
    def asks_time(body):
        time_questions = ['ʻO ka hola ʻehia kēia?',
                          "'O ka hola 'ehia keia?",
                          'What time is it?',
                          "What's the time?"]
        for q in time_questions:
            if q.lower() in body.lower(): return True
        return False

    @staticmethod
    def build_time(name):
        ts = taw.time_to_words("now")
        return f"E @{name}, " + ts

    def post_time_reply(self, status_id, body):
        api = self.API
        if self.DEBUG:
            print(f"{status_id} gets the tweet: {body}")
        else:
            api.update_status(status=body,
                              in_reply_to_status_id_str=status_id)

    @staticmethod
    def build_link(screen_name, tweet_id):
        return f"https://twitter.com/{screen_name}/status/{tweet_id}"

    def post_time_retweet(self, reply_to, user):
        api = self.API
        body = f"{self.build_time(user._json['screen_name'])} {self.build_link(user._json['screen_name'], reply_to._json['id_str'])}"
        if self.DEBUG:
            print(body)
        else:
            try:
                api.update_status(status=body,
                                  in_reply_to_status_id_str=reply_to._json['id_str'])
            except tweepy.error.TweepError as e:
                print(e)

    def check_tweets(self):
        api = self.API
        recent_tweets = api.mentions_timeline(count=100)
        for rt in recent_tweets:
            if rt._json['id_str'] in self.last_reqs:
                continue
            self.last_reqs.appendleft(rt._json['id_str'])
            if self.asks_time(rt._json['text']):
                user = api.get_user(user_id=rt._json['user']['id'])
                #self.post_time_reply(status_id=rt._json['id_str'],
                #                     body=self.build_time(user._json['screen_name']))
                self.post_time_retweet(reply_to=rt,
                                       user=user)
        with open(os.path.join('../tmp', 'last_reqs.pickle'), 'wb') as fh:
            pickle.dump(self.last_reqs, fh)

    def speaking_clock(self):
        clock_is_on = True
        while clock_is_on:
            print("Checking for times...")
            self.check_tweets()
            time.sleep(300)

if __name__ == '__main__':
    t = TweeterSpeakingClock(debug=False)
    t.speaking_clock()