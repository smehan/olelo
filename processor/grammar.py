###########################################################
# Copyright (C) 2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Processor for transforming source html into usable data.
# This module defines general grammatical maps and constants
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

__all__ = ['HAW_POS', 'DIGITS', 'HAW_ALPHABET']

HAW_POS = {'a-class possessive': ['a-poss.'],
           'adverb': ['adverb'],
           'adjective': ['adj.'],
           'antonym': ['ant.'],
           'article': ['art.'],
           'causative/simulative': ['caus/sim.'],
           'conjunction': ['conj.'],
           'demonstrative': ['demon.'],
           'directional': ['dir'],
           'exclusive': ['excl.'],
           'figuratively': ['fig.'],
           'frequantive': ['freq.'],
           'idiom': ['idiom.'],
           'inclusive': ['incl.'],
           'imperative': ['imper.'],
           'interjection': ['interj.'],
           'interrogative': ['interr.'],
           'intransitive verb': ['vi.', 'nvi.'],
           'locative noun': ['loc n.'],
           'nominalizer': ['nom.'],
           'noun-verb': ['nv.'],
           'noun': ['n.', 'nvi.', 'nvt.', 'nvs.', 'loc n.', 'nv.'],
           'o-class possessive': ['o-poss.'],
           'particle': ['part.', 'particle', 'prep.'],
           'passive/imperative': ['pas/imp.'],
           'possessive': ['poss.', 'a-poss.', 'o-poss.'],
           'pronoun': ['pro.', 'pronoun'],
           'preposition': ['prep.'],
           'perfect participle': ['perf.part.'],
           'reduplication': ['redup.'],
           'stative verb': ['vs.', 'nvs.'],
           'transitive verb': ['vt.', 'nvt.'],
           'transitivizer': ['transitivizer'],
           'verb': ['v.', 'vt.', 'vi.', 'vs.', 'nvi.', 'nvs.', 'nvt.', 'nv.']}

""" These should be normalizations to modern Hawaiian that reflect beginning consonant changes k -> v"""
HAW_SPELLING_NORMALIZATIONS = {'b': 'p',
                               'd': 'k'}

# TODO syns, Plural, Lit, antonyms

DIGITS = '0123456789'
HAW_ALPHABET = 'aāeēhiīklmnoōpuūwʻ'


if __name__ == '__main__':
    print(f"This is {__name__}")
