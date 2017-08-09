###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Class to instantiate a twitter stream listener to listen for requests for
# answering what time is it.
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import os
import time
import datetime as dt
from qr import CappedCollection

# 3rd-party libs
import tweepy

# application libs
from twitter.tweeter import Tweeter
import translations.time_as_words as taw


class TweeterSpeakingClock(Tweeter):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.last_reqs = CappedCollection('speaking_clock_reqs', 100)

    @staticmethod
    def _asks_time(body):
        time_questions = ['ʻO ka hola ʻehia kēia',
                          "'O ka hola 'ehia keia",
                          'What time is it',
                          "What's the time"]
        for q in time_questions:
            if q.lower() in body.lower(): return True
        return False

    def is_stale(self, t: tweepy, period=3.0) -> bool:
        """
        Determine if the tweet is older than period
        :param t: a Tweepy object with a datetime attr
        :param period: the period of time beyond which a tweet is considered stale
        :return:
        """
        if self.twitter_now() - self.twitter_time(t.created_at) > dt.timedelta(hours=period):
            return True
        return False

    @staticmethod
    def _build_time(name: str) -> str:
        ts = taw.time_to_words("now")
        return f"E @{name}, " + ts

    def post_time_reply(self, status_id, body: str):
        api = self.API
        if self.DEBUG:
            self.logger.debug(f"{status_id} gets the tweet: {body}")
        else:
            api.update_status(status=body,
                              in_reply_to_status_id_str=status_id)

    @staticmethod
    def build_link(screen_name: str, tweet_id: str) -> str:
        return f"https://twitter.com/{screen_name}/status/{tweet_id}"

    def post_time_retweet(self, reply_to: tweepy, user: tweepy):
        api = self.API
        body = f"{self._build_time(user._json['screen_name'])} {self.build_link(user._json['screen_name'], reply_to._json['id_str'])}"
        if self.DEBUG:
            self.logger.debug(body)
        else:
            try:
                api.update_status(status=body,
                                  in_reply_to_status_id_str=reply_to._json['id_str'])
            except tweepy.error.TweepError as e:
                self.logger.error(e)

    def check_tweets(self):
        api = self.API
        recent_tweets = api.mentions_timeline(count=100)
        for rt in recent_tweets:
            if rt._json['id_str'] in self.last_reqs:
                continue
            if self.is_stale(rt.created_at):
                continue
            self.last_reqs.push(rt._json['id_str'])
            if rt._json['user']['screen_name'] == "Kaka_Olelo":
                continue
            if self._asks_time(rt._json['text']):
                user = api.get_user(user_id=rt._json['user']['id'])
                #self.post_time_reply(status_id=rt._json['id_str'],
                #                     body=self._build_time(user._json['screen_name']))
                self.post_time_retweet(reply_to=rt,
                                       user=user)

    def speaking_clock(self):
        clock_is_on = True
        while clock_is_on:
            self.logger.info(f"Checking for times...")
            self.check_tweets()
            time.sleep(30)

if __name__ == '__main__':
    t = TweeterSpeakingClock(debug=True)
    t.speaking_clock()