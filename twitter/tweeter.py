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
from persistance.redis_db import RedisDB


class Tweeter(RedisDB):
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

        self.DEBUG = debug

    def print_tweets(self):
        api = self.API
        data = api.user_timeline(screen_name=self.screen_name, count=100, include_rts=True)
        for d in data:
            return d._json['text']

    def push_tweet(self, hw, defs):
        api = self.API
        tweet = f"#HawaiianWOTD: {hw} - {defs}"
        if self.DEBUG:
            print(f'About to tweet: {tweet}')
        else:
            status = api.update_status(status=tweet)

    def make_tweet_of_day(self):
        huid = self._get_random_key()
        hw_hash = self._all_hash('haw:id')
        for k, v in hw_hash.items():
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
                    print(f"friended {user.id}")
                    api.create_friendship(id=user.id)
                    found_one = True
                    break
            page += 1


if __name__ == "__main__":
    t = Tweeter(debug=True)
    print(t.print_tweets())
    t.make_tweet_of_day()
    t.find_a_new_friend()
