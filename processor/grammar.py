###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Processor for transforming source html into usable data
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs

# 3rd-party libs

# application libs

# Want to build a single dict for all dict abbrevs.
# Need to be able to find symbol for all entries.
# Not certain how to match compound symbol to multiple entries, e.g.
# nvi. 1. a thing; to be a thing....

__all__ = ['HAW_POS']

HAW_POS = {'noun': ['n.', 'nvi.', 'nvt.', 'nvs.'],
           'interjection': ['interj.'],
           'verb': ['v.'],
           'intransitive verb': ['vi.', 'nvi.'],
           'transitive verb': ['vt.', 'nvt.'],
           'stative verb': ['vs.', 'nvs.'],
           'plural': ['Plural'],
           'reduplication': ['Redup.'],
           'passive/imperative': ['Pas/imp.'],
           'adjective': ['adj.'],
           'adverb': ['adverb'],
           'antonym': ['ant.'],
           'conjunction': ['conj.'],
           'figuratively': ['fig.'],
           'frequantive': ['freq.'],
           'imperative': ['imper.'],
           'literally': ['Lit.'],
           'pronoun': ['pro.', 'pronoun.'],
           'preposition': ['prep.'],
           'perfect participle': ['perf.part.'],
           'synonym': ['Syn']}


if __name__ == '__main__':
    print(f"This is {__name__}")
