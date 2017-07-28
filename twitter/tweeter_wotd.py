###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Class to drive WOTD for twitter
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs
import itertools

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
            print(f'About to tweet: {tweet}')
        else:
            status = api.update_status(status=tweet)

    def make_tweet_of_day(self):
        huid = self._get_random_key()
        hw_hash = self._all_hash('haw:id')
        for k, v in iter(hw_hash.items()):
            if v == huid:
                word_defs = self._all_values_from_hash(':'.join(['defs', huid]))
                word_pos = self.rdb.smembers(':'.join(['pos', huid]))
                print(f'POS - {word_pos}')
                self.push_tweet(k, word_defs)

    def find_a_new_friend(self):
        api = self.API
        page = 0
        found_one = False
        while not found_one:
            result = api.search_users('#hawaiian', page=page)
            for user in result:
                if user.following is False and 'hawaii' in user.description.lower():
                    try:
                        print(f"friended {user.id}")
                        api.create_friendship(id=user.id)
                        found_one = True
                        break
                    except tweepy.error.TweepError as e:
                        print(e)
            page += 1


if __name__ == "__main__":
    t = TweeterWOTD(debug=True)
    print(t.print_tweets())
    t.make_tweet_of_day()
    t.find_a_new_friend()
