# Redis_DB

There is a base class for interacting with the Redis DB
that holds the hawaiin dictionary. Inherit from *RedisDB*
and extend with any additional methods needed.

## Redis Schema

All keys should follow general schema of *\<name>*:*\<id>* 

1. haw:id - \<hawaiian headword>:<sha1> hash of that headword
2. pos:\<id> - set of pos true for this headword
3. content:\<id> - set of content entries for this headword

# backlog
1. should this and twitter be singletons or even borgs? http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
