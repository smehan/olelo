# Redis_DB
There is a base class for interacting with the Redis DB
that holds the hawaiin dictionary. Inherit from *RedisDB*
and extend with any additional methods needed.

## Redis Schema

All keys should follow general schema of *\<name>*:*\<id>* 

1. haw:id - \<hawaiian headword>:<sha1> hash of that headword
2. pos:\<id> - set of pos true for this headword
