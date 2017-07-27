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

# application libs
from twitter.tweeter import Tweeter
import translations.time_as_words as taw


class TweeterSpeakingClock(Tweeter):

    def __init__(self, **kargs):
        super().__init__(**kargs)

        pickle_path = os.path.join(os.path.dirname(os.path.abspath(__file__)).rsplit("/", 1)[0], 'tmp', 'last_reqs.pickle')
        if os.path.isfile(pickle_path):
            with open(pickle_path, 'rb') as fh:
                self.last_reqs = pickle.load(fh)
        else:
            open(pickle_path, 'w').close()
            self.last_reqs = deque(maxlen=100)

    @staticmethod
    def asks_time(body):
        time_questions = ['ʻO ka hola ʻehia kēia',
                          "'O ka hola 'ehia keia",
                          'What time is it',
                          "What's the time"]
        for q in time_questions:
            if q.lower() in body.lower(): return True
        return False

    @staticmethod
    def build_time(name: str) -> str:
        ts = taw.time_to_words("now")
        return f"E @{name}, " + ts

    def post_time_reply(self, status_id, body: str):
        api = self.API
        if self.DEBUG:
            print(f"{status_id} gets the tweet: {body}")
        else:
            api.update_status(status=body,
                              in_reply_to_status_id_str=status_id)

    @staticmethod
    def build_link(screen_name: str, tweet_id: str) -> str:
        return f"https://twitter.com/{screen_name}/status/{tweet_id}"

    def post_time_retweet(self, reply_to: tweepy, user: tweepy):
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
            if rt._json['user']['screen_name'] == "Kaka_Olelo":
                continue
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
            time.sleep(30)

if __name__ == '__main__':
    t = TweeterSpeakingClock(debug=False)
    t.speaking_clock()