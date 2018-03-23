from redis import StrictRedis
import os
import hashlib
import json

redis = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"), 
                    port=os.environ.get("REDIS_PORT", 6379),
                    db=0)

p = redis.pipeline()

events = [
  { 'sku': "123-ABC-723",
    'name': "Men's 100m Final",
    'disabled_access': True,
    'medal_event': True,
    'venue': "Olympic Stadium",
    'category': "Track & Field"
  },
  { 'sku': "737-DEF-911",
    'name': "Women's 4x100m Heats",
    'disabled_access': True,
    'medal_event': False,
    'venue': "Olympic Stadium",
    'category': "Track & Field"
  },
  { 'sku': "320-GHI-921",
    'name': "Womens Judo Qualifying",
    'disabled_access': False,
    'medal_event': False,
    'venue': "Nippon Budokan",
    'category': "Martial Arts"
  }      
]

def create_events(events):
  for i in range(len(events)):
    redis.set('event:' + events[i]['sku'], json.dumps(events[i]))

# Create events
create_events(events)

# Match Method 1 - Object inspection
# Find all matching keys, retreive value and then exeamine for all macthing attributes

def match_by_inspection(*keys):
  m = []
  for key in redis.scan_iter('event:*'):
    match = False
    event = json.loads(redis.get(key))
    for kv in keys:
      k, v = kv
      if k in event and event[k] == v:
        match = True
      else:
        match = False
        break
    if match:
        m.append(event['sku'])
  return m

# Find the match
matches = match_by_inspection(('disabled_access', True))
for m in matches:
  print json.loads(redis.get('event:' + m)) 

matches = match_by_inspection(('disabled_access', True), ('medal_event', False))
for m in matches:
  print json.loads(redis.get('event:' + m)) 

matches = match_by_inspection(('disabled_access', False), ('medal_event', False), ('venue', "Nippon Budokan"))
for m in matches:
  print json.loads(redis.get('event:' + m)) 


# Match method 2 - Faceted Search
# For each attribute & value combination, add the event into a Set
lookup_attrs = ['disabled_access', 'medal_event', 'venue', 'tbd']

def create_events_with_lookups(events):
  for i in range(len(events)):
    redis.set('event:' + events[i]['sku'], json.dumps(events[i]))
    for k in range(len(lookup_attrs)):
      if lookup_attrs[k] in events[i]:
        redis.sadd("fs:" + lookup_attrs[k] + ":" + str(events[i][lookup_attrs[k]]), events[i]['sku'])

# Create events
create_events_with_lookups(events)

def match_by_faceting(*keys):
  fs = []
  for kv in keys:
    k, v = kv
    fs.append("fs:" + k + ":" + str(v))
  return redis.sinter(fs)

# Find the match
matches = match_by_faceting(('disabled_access', True))
for m in matches:
  print json.loads(redis.get('event:' + m)) 

matches = match_by_faceting(('disabled_access', True), ('medal_event', False))
for m in matches:
  print json.loads(redis.get('event:' + m)) 

matches = match_by_faceting(('disabled_access', False), ('medal_event', False), ('venue', "Nippon Budokan"))
for m in matches:
  print json.loads(redis.get('event:' + m)) 

# Match method 3 - Hashed Faceted Search
def create_events_with_hashed_lookups(events):
  for i in range(len(events)):
    redis.set('event:' + events[i]['sku'], json.dumps(events[i]))
    hfs = []
    for k in range(len(lookup_attrs)):
      if lookup_attrs[k] in events[i]:
        hfs.append((lookup_attrs[k], events[i][lookup_attrs[k]]))
      redis.sadd("hfs:" + hashlib.sha256(str(hfs)).hexdigest(), events[i]['sku'])

# Create events
create_events_with_hashed_lookups(events)

def match_by_hashed_faceting(*keys):
  m = []  
  hfs = []
  for i in range(len(lookup_attrs)):
    k = [x for x in keys if x[0] == lookup_attrs[i]]
    if k:
      hfs.append(k[0])
  for k in redis.sscan_iter("hfs:" + hashlib.sha256(str(hfs)).hexdigest())
    m.append(k)
  return m

# Find the match
matches = match_by_hashed_faceting(('disabled_access', True))
for m in matches:
  print json.loads(redis.get('event:' + m)) 

matches = match_by_hashed_faceting(('disabled_access', True), ('medal_event', False))
for m in matches:
  print json.loads(redis.get('event:' + m)) 

matches = match_by_hashed_faceting(('disabled_access', False), ('medal_event', False), ('venue', "Nippon Budokan"))
for m in matches:
  print json.loads(redis.get('event:' + m)) 

