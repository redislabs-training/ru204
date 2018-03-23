from redis import StrictRedis
import os
import hashlib
import json
import random
from faker import Faker
import string

redis = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"), 
										port=os.environ.get("REDIS_PORT", 6379),
										db=0)


fake = Faker()
p = redis.pipeline()

def generate_cust_id():
	return ''.join(random.choice(string.ascii_uppercase + string.digits) \
		for _ in range(8))

def create_customers(num):
	fake.seed(94002)
	for _ in range(num):
		id = generate_cust_id()
		p.hmset("customer:" + id, {'full_name': fake.name(), 'address': fake.address(), 'phone': fake.phone_number()})
		p.execute()

create_customers(4002)

ticket_tiers = ["Lottery", "General", "Reserved", "VIP"]

def create_event(event, venue, capacity=None, geo=None):
	p.sadd("events", event)
	p.sadd("event:" + event + ":venues" , venue)
	if capacity is not None:
		event_capacity = random.randint(capacity/10, capacity/2)
		attrs = {	'venue': venue, 
							'capacity': event_capacity,
							'medal_event' : fake.random_element((True, False)),
							'disabled_access' : fake.random_element((True, False))}
		tiers_availbale = random.randint(1,3)
		event_remaining = event_capacity
		for k in range(tiers_availbale, 0, -1):
			tier_availability = random.randint(((event_capacity/tiers_availbale))/2, (event_capacity/tiers_availbale)) 
			event_remaining = event_remaining - tier_availability
			attrs["availability:" + ticket_tiers[k]] = tier_availability if (k != 0 ) else event_remaining 
			attrs["price:" + ticket_tiers[k]] = random.randint(10 * (k+1), 10 * (k+1) + 9)
		p.hmset("event:" + event + ":" + venue, attrs)
	if geo is not None:
		p.geoadd("event:" + event + ":geo", geo['long'], geo['lat'], venue)


def create_transit(transit, venue, geo=None):
		p.sadd("transit:" + transit + ":events", venue)
		if geo is not None:
			p.geoadd("transit:" + transit + ":geo", geo['long'], geo['lat'], venue)

def create_venues(fn="/data/venues.json"):
	random.seed(94002)
	f = open(fn)
	venues = json.load(f)
	for i in range(len(venues)):
		v = venues[i]
		attrs = {'zone': v['zone']}
		if 'capacity' in v:
			attrs['capacity'] = v['capacity']
		p.hmset("venue:" + v['venue'], attrs)
		p.sadd("venues", v['venue'])
		for k in range(len(v['events'])):
			p.sadd("venue:" + v['venue'] + ":events", v['events'][k])
			create_event(v['events'][k], 
									 v['venue'],
									 v['capacity'] if ('capacity' in v) else None,
									 v['geo'] if ('geo' in v) else None)
		if 'transit' in v:
			for k in range(len(v['transit'])):
				create_transit(v['transit'][k],
											 v['venue'],
											 v['geo'] if ('geo' in v) else None)
	if 'geo' in v:
			p.geoadd("venue:locations", v['geo']['long'], v['geo']['lat'], v['venue'])
	p.execute()

create_venues()
