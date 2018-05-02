"""Utility to dump and load keys from Redis. Key value sare encoded in JSON. In
this module the following functions are available:

	* dump(fn, compress, match)
	* load(fn, compress)

"""
from redis import StrictRedis
import os
import json
import base64
import gzip

redis = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"), 
										port=os.environ.get("REDIS_PORT", 6379),
										db=0)


def dump(fn="/data/ru101.json", compress=False, match="*"):
	count = 0
	try:
		if compress:
			f = gzip.open(fn, "wb")
		else:
			f = open(fn, "w")
		for k in redis.scan_iter(match):
			obj = {}
			t = redis.type(k)
			obj['t'] = t
			obj['k'] = k
			obj['ttl'] = redis.ttl(k)
			if t == "hash":
				obj['v'] = redis.hgetall(k)
			elif t == "set":
				obj['v'] = list(redis.smembers(k))
			elif t == "zset":
				obj['v'] = redis.zrange(k, 0, -1, withscores=True)
			elif t == "list":
				obj['v'] = redis.lrange(k, 0, -1)
			elif t == "string":
				encoding = redis.object("encoding", obj['k'])
				obj['e'] = encoding
				if encoding == "embstr":
					obj['v'] = redis.get(k)
				elif encoding == "raw":
					obj['v'] = base64.b64encode(bytearray(redis.get(k)))
				else:
					print "got a string encoded as {}".format(encoding)
					continue
			else:
				print "got a type I don't do: {}".format(t)
				continue
			count += 1
			f.write(json.dumps(obj))
			f.write("\n") 
	finally:	
		f.close()
		print "total keys dumped: {}".format(count)

def load(fn="/data/ru101.json", compress=False):
	count=0
	try:
		p = redis.pipeline()
		if compress:
			f = gzip.open(fn, "rb")
		else:
			f = open(fn, "r")
		line = f.readline()
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
				if obj['e'] == "string":
					p.set(obj['k'], obj['v'])
				elif obj['e'] == "raw":					
					p.set(obj['k'], base64.b64decode(obj['v']))
			else:
				print "got a type I don't do: {}".format(obj['t'])
				continue
			if 'ttl' in obj and obj['ttl'] >=0:
				p.expire(obj['k'], obj['ttl'])
			p.execute()
			line = f.readline()
			count += 1
	finally:
		f.close()
		print "total keys loaded: {}".format(count)

