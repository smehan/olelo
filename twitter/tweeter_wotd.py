###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Class to drive WOTD for twitter
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs

# 3rd-party libs
import tweepy

# application libs
from persistance.redis_db import RedisDB
from twitter.tweeter import Tweeter


class TweeterWOTD(Tweeter, RedisDB):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def push_tweet(self, hw, defs):
        api = self.API
        tweet = f"#Hawaiian: {hw} - {defs}"
        if self.DEBUG:
            self.logger.info(f'About to tweet: {tweet}')
        else:
            status = api.update_status(status=tweet)

    @staticmethod
    def _clean_line(text: str) -> str:
        """Remove unneeded characters from string"""
        UNNEEDED_CHARS = ['[', ']', "'"]
        ALT_TEXT = {'Cf.': 'See also'}
        for c in UNNEEDED_CHARS:
            text.replace(c, '')
        for k, v in ALT_TEXT.items():
            text.replace(k, v)
        return text

    def clean_text(self, text):
        """Remove unneeded characters from definitions body"""
        if isinstance(text, str):
            new_text = self._clean_line(text)
        elif isinstance(text, list):
            new_text = []
            for e in text:
                new_text.append(self._clean_line(e))
        return new_text

    def make_tweet_of_day(self):
        huid = self._get_random_key()
        hw_hash = self._all_hash('haw:id')
        for k, v in iter(hw_hash.items()):
            if v == huid:
                word_defs = self._all_values_from_hash(':'.join(['defs', huid]))
                word_pos = self.rdb.smembers(':'.join(['pos', huid]))
                self.logger.info(f'POS - {word_pos}')
                nt = self.clean_text(word_defs)
                self.push_tweet(k, nt)
                return

    def find_a_new_friend(self):
        api = self.API
        page = 0
        found_one = False
        while not found_one:
            result = api.search_users('#hawaiian', page=page)
            for user in result:
                if user.following is False and 'hawaii' in user.description.lower():
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
    t.make_tweet_of_day()
    #t.find_a_new_friend()
