# Ōlelo - Hawaiian language web platform

#### Build status: [![Build Status](https://travis-ci.org/smehan/olelo.svg?branch=master)](https://travis-ci.org/smehan/olelo)


## Redis Schema
*presistance.load_dict.py* will load a pickled dictionary into the following redis schema. It expects a localhost redis, configured through *persistance.redis_db.py*

* Key *haw:id* redis hash with a key value pairs = {hawaiian headword, hash_id}. This is the lookup hash for every headword and yields the hash id against which each of the other keys operates.
* Key *defs:id* redis hash with key value pairs = {number: definition}
* Key *pos:id* redis list of parts of speech for this headword.
* Key *content:id* redis set of each content line parsed from source docs.