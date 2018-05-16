"""Utility to dump and load keys from Redis. Key values are encoded in JSON. In
this module the following functions are available:

  * dump(fn, compress, match)
  * load(fn, compress)

"""
from redis import StrictRedis
import os
import sys


def dump(r, filename="/data/ru101.json", compress=False, match="*"):
  """Dump matching keys into JSOn file format"""
  import json
  import base64
  import gzip

  count = 0
  try:
    if compress:
      fn = gzip.open(filename, "wb")
    else:
      fn = open(filename, "w")
    for k in r.scan_iter(match):
      obj = {}
      t = r.type(k)
      obj['t'] = t
      obj['k'] = k
      obj['ttl'] = r.ttl(k)
      if t == "hash":
        obj['v'] = r.hgetall(k)
      elif t == "set":
        obj['v'] = list(r.smembers(k))
      elif t == "zset":
        obj['v'] = r.zrange(k, 0, -1, withscores=True)
      elif t == "list":
        obj['v'] = r.lrange(k, 0, -1)
      elif t == "string":
        encoding = r.object("encoding", obj['k'])
        obj['e'] = encoding
        if encoding == "embstr":
          obj['v'] = r.get(k)
        elif encoding == "raw":
          obj['v'] = base64.b64encode(bytearray(r.get(k)))
        else:
          print "got a string encoded as {}".format(encoding)
          continue
      else:
        print "got a type I don't do: {}".format(t)
        continue
      count += 1
      fn.write(json.dumps(obj))
      fn.write("\n")
  finally:
    fn.close()
    print "total keys dumped: {}".format(count)

def load(r, filename="/data/ru101.json", compress=False):
  """Load keys from file in JSON format"""
  import json
  import base64
  import gzip

  count = 0
  if compress:
    fn = gzip.open(filename, "rb")
  else:
    fn = open(filename, "r")
  try:
    line = fn.readline()
    p = r.pipeline()
    while line:
      obj = json.loads(line)
      p.delete(obj['k'])
      if obj['t'] == "hash":
        p.hmset(obj['k'], obj['v'])
      elif obj['t'] == "set":
        for j in range(len(obj['v'])):
          p.sadd(obj['k'], obj['v'][j])
      elif obj['t'] == "zset":
        for j in range(len(obj['v'])):
          v, s = obj['v'][j]
          p.zadd(obj['k'], s, v)
      elif obj['t'] == "list":
        for j in range(len(obj['v'])):
          p.rpush(obj['k'], obj['v'][j])
      elif obj['t'] == "string":
        if obj['e'] == "embstr":
          p.set(obj['k'], obj['v'])
        elif obj['e'] == "raw":
          p.set(obj['k'], base64.b64decode(obj['v']))
      else:
        print "got a type I don't do: {}".format(obj['t'])
        continue
      if 'ttl' in obj and obj['ttl'] >= 0:
        p.expire(obj['k'], obj['ttl'])
      p.execute()
      count += 1
      line = fn.readline()
  finally:
    fn.close()
    print "total keys loaded: {}".format(count)

if __name__ == "__main__":
  r = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"),
                    port=os.environ.get("REDIS_PORT", 6379),
                    db=0)
  if sys.argv[1] == "load":
    load(r, filename=sys.argv[2])
  elif sys.argv[1] == "dump":
    dump(r, filename=sys.argv[2])

