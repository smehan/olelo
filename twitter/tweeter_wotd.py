###########################################################
# Copyright (C) 2018 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Class to drive WOTD for twitter
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
from itertools import chain

# 3rd-party libs
import tweepy

# application libs
from persistance.redis_db import RedisDB
from twitter.tweeter import Tweeter


class TweeterWOTD(Tweeter, RedisDB):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.MAX_LENGTH = 280

    def push_tweet(self, hw, defs):
        api = self.API
        tweet = f"#Hawaiian: {hw} - {defs}"
        if self.DEBUG:
            if not self.is_good_length(tweet):
                self.logger.warn(f'TOO LONG: {len(tweet)}')
            self.logger.info(f'About to tweet: {tweet}')
        else:
            status = api.update_status(status=tweet)

    def is_good_length(self, tweet):
        """Checks a tweet for length of less than Max"""
        if len(tweet) >= self.MAX_LENGTH:
            return False
        return True

    @staticmethod
    def _clean_line(s: str)-> str:
        """Remove unneeded characters from string"""
        UNNEEDED_CHARS = ['[', ']', "'"]
        ALT_TEXT = {'Cf.': 'See also',
                    'Lit.': 'Literally'}
        for c in UNNEEDED_CHARS:
            s.replace(c, '')
        for k, v in ALT_TEXT.items():
            s.replace(k, v)
        return s

    def form_def(self, defs)-> str:
        """Form a str to use as the tweet def"""
        if isinstance(defs, str):
            new_defs = self._clean_line(defs)
        elif isinstance(defs, list):
            new_list = []
            for e in defs:
                new_list.append(self._clean_line(e))
            new_defs = " ".join(new_list)
        return new_defs

    def make_tweet_of_day(self):
        huid = self._get_random_key()
        hw_hash = self._all_hash('haw:id')
        for k, v in iter(hw_hash.items()):
            if v == huid:
                word_defs = self._all_values_from_hash(':'.join(['defs', huid]))
                word_pos = self.rdb.smembers(':'.join(['pos', huid]))
                self.logger.info(f'POS - {word_pos}')
                self.push_tweet(k, self.form_def(word_defs))
                return

    @staticmethod
    def is_good_description(desc: str)-> bool:
        """Checks user description against a set of eval criteria to
            determine if this is a good description to follow
        """
        d = desc.lower()
        if 'hawaii' in d and 'shirt' not in d:
            return True
        return False

    def find_a_new_friend(self):
        api = self.API
        page = 0
        found_one = False
        # if already tweeted today, don't add friends ...
        if self.tweeted_today():
            return
        while not found_one:
            result = api.search_users('#hawaiian', page=page)
            for user in result:
                if user.following is False and self.is_good_description(user.description):
                    try:
                        self.logger.info(f"friended {user.id}")
                        api.create_friendship(id=user.id)
                        found_one = True
                        break
                    except tweepy.error.TweepError as e:
                        self.logger.error(e)
            page += 1


if __name__ == "__main__":
    t = TweeterWOTD(debug=True)
    print(t.print_tweets())
    t.find_a_new_friend()
    t.make_tweet_of_day()
