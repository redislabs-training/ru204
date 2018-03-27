from redis import StrictRedis
import os
import json
import gzip

redis = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"), 
										port=os.environ.get("REDIS_PORT", 6379),
										db=0)


def dump(fn="/data/ru101.json", compress=False, match="*"):
	if compress:
		f = gzip.open(fn, "wb")
	else:
		f = open(fn, "w")
	count = 0
	for k in redis.scan_iter(match):
		obj = {}
		t = redis.type(k)
		obj['t'] = t
		obj['k'] = k
		obj['ttl'] = redis.ttl(k)
		if t == "hash":
			obj['v'] = redis.hgetall(k)
		elif t == 'set':
			obj['v'] = list(redis.smembers(k))
		elif t == 'zset':
			obj['v'] = redis.zrange(k, 0, -1, withscores=True)
		elif t == 'list':
			obj['v'] = redis.lrange(k, 0, -1)
		else:
			print "got a type I don't do:", t
			continue
		count += 1
		f.write(json.dumps(obj))
		f.write("\n")
	f.close()
	print "total keys dumped:", count

def load(fn="/data/ru101.json", compress=False):
	p = redis.pipeline()
	count=0
	if compress:
		f = gzip.open(fn, "rb")
	else:
		f = open(fn, "r")
	line = f.readline()
	while line:
		obj = json.loads(line)
		redis.delete(obj['k'])
		if obj['t'] == "hash":
			p.hmset(obj['k'], obj['v'])
		elif obj['t'] == 'set':
			for j in range(len(obj['v'])):
				p.sadd(obj['k'], obj['v'][j])
		elif obj['t'] == 'zset':
			for j in range(len(obj['v'])):
				v, s = obj['v'][j]
				p.zadd(obj['k'], s, v)
		elif obj['t'] == 'list':
			for j in range(len(obj['v'])):
				p.rpush(obj['k'], obj['v'][j])
		else:
			print "got a type I don't do:", obj['t']
			continue
		if 'ttl' in obj and obj['ttl'] >=0:
			p.expire(obj['k'], obj['ttl'])
		p.execute()
		line = f.readline()
		count += 1
	f.close()
	print "total keys loaded:", count

