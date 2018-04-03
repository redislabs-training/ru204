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
	return fake.pystr(min_chars=8, max_chars=8).upper()

def generate_sku():
	return "{0}-{1}-{2}-{3}".format(fake.pystr(min_chars=4, max_chars=4), fake.pystr(min_chars=4, max_chars=4), 
																	fake.pystr(min_chars=4, max_chars=4), fake.pystr(min_chars=4, max_chars=4)).upper()

def generate_order_id():
	return "{0}-{1}".format(fake.pystr(min_chars=6, max_chars=6), fake.pystr(min_chars=4, max_chars=6)).upper()

customers = []
def create_customers(num):
	fake.seed(94002)
	for _ in range(num):
		id = generate_cust_id()
		p.hmset("customer:" + id, {'customer_name': fake.name(), 'address': fake.address(), 'phone': fake.phone_number()})
		p.sadd("customers", id)
		p.execute()
		customers.append(id)

create_customers(501)

ticket_tiers = ["Lottery", "General", "Reserved", "VIP"]

events = []
def create_event(event, venue, capacity=None, geo=None, add_faceted_search=False, add_hashed_search=False):
	sku = generate_sku()
	p.sadd("events", sku)
	p.sadd("event:skus:" + event, sku)
	p.sadd("event:venues:" + sku, venue)
	attrs = {	'name': event,
						'venue': venue, 
						'medal_event' : fake.random_element((True, False)),
						'disabled_access' : fake.random_element((True, False))}
	if capacity is not None:
		event_capacity = random.randint(capacity/10, capacity/2)
		attrs['capacity'] = event_capacity
		tiers_availbale = random.randint(1,3)
		event_remaining = event_capacity
		for k in range(tiers_availbale, 0, -1):
			tier_availability = random.randint(((event_capacity/tiers_availbale))/2, (event_capacity/tiers_availbale)) 
			event_remaining = event_remaining - tier_availability
			attrs['available:' + ticket_tiers[k]] = tier_availability if (k != 0 ) else event_remaining 
			attrs['price:' + ticket_tiers[k]] = random.randint(10 * (k+1), 10 * (k+1) + 9)
		p.hmset("event:" + sku, attrs)
	attrs['sku'] = sku
	if geo is not None:
		p.geoadd("event:geo:" + event, geo['long'], geo['lat'], venue)
	if add_faceted_search:
		create_faceted_search(attrs)
	if add_hashed_search:
		create_hashed_search(attrs)
	events.append(sku)
	return attrs

search_attrs = ['medal_event', 'disabled_access', 'venue']

def create_faceted_search(obj, key="sku", attrs=search_attrs):
	for k in range(len(search_attrs)): 
		if search_attrs[k] in obj:
			redis.sadd("fs:" + search_attrs[k] + ":" + str(obj[search_attrs[k]]), obj[key] if (key in obj) else None)

def create_hashed_search(obj, key="sku", attrs=search_attrs):
	hfs = []
	for k in range(len(search_attrs)):
		if search_attrs[k] in obj:
			hfs.append((search_attrs[k], obj[search_attrs[k]]))
	redis.sadd("hfs:" + hashlib.sha256(str(hfs)).hexdigest(), obj[key] if (key in obj) else None)

def create_transit(transit, venue, event_sku, geo=None):
		p.sadd("transit:" + transit + ":events", event_sku)
		if geo is not None:
			p.geoadd("transit:geo:" + transit, geo['long'], geo['lat'], venue)

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
			e = create_event(v['events'][k], 
											 v['venue'],
											 v['capacity'] if ('capacity' in v) else None,
											 v['geo'] if ('geo' in v) else None,
											 True,
											 True)
			p.sadd("venue:" + v['venue'] + ":events", e['sku'])
		if 'transit' in v:
			for k in range(len(v['transit'])):
				create_transit(v['transit'][k],
											 v['venue'],
											 e['sku'],
											 v['geo'] if ('geo' in v) else None)
		if 'geo' in v:
				p.geoadd("venues:geo", v['geo']['long'], v['geo']['lat'], v['venue'])
		p.execute()

create_venues()

def create_orders(num_customers=100, max_orders_per_customer=5):
	for i in range(num_customers):
		num_orders = random.randint(1, max_orders_per_customer)
		customer_id = customers[random.randint(0, len(customers)-1)]
		customer_name = redis.hget("customer:" + customer_id, "customer_name")
		for j in range(num_orders):
			order_id = generate_order_id()
			event_sku = events[random.randint(0, len(events)-1)]
			for k in range(len(ticket_tiers)-1, 0, -1):
				if redis.hexists("event:" + event_sku, "available:" + ticket_tiers[k]):
					price = float(redis.hget("event:" + event_sku, "price:" + ticket_tiers[k]))
					availbale = long(redis.hget("event:" + event_sku, "available:" + ticket_tiers[k]))
					event_name = redis.hget("event:" + event_sku, "name")
					if availbale > 1:
						qty = random.randint(1, availbale/2)
					elif availbale == 1:
						qty = 1
					else:
						continue
					purchase = {	'customer': customer_id, 'customer_name': customer_name,
												'order_id': order_id, 'event': event_sku, 'event_name': event_name,
												'tier': ticket_tiers[k], 'qty': qty, 'cost': qty * price, 
												'ts': long(time.time()) }	
					p.hmset("sales_order:" + order_id, purchase)
					p.hincrby("event:" + event_sku, "available:" + ticket_tiers[k] , qty * -1)
					p.sadd("sales_orders:" + event_sku, order_id)
					p.sadd("invoices:" + customer_id, order_id)
					p.hincrbyfloat("sales_summary", "total_sales:" + event_name, qty * price)
					p.hincrby("sales_summary", "total_tickets_sold:" + event_name, qty)
					p.hincrbyfloat("sales_summary", "total_sales:" + event_name + ":" + ticket_tiers[k], qty * price)
					p.hincrby("sales_summary", "total_tickets_sold:" + event_name + ":" + ticket_tiers[k], qty)
					p.hincrbyfloat("sales_summary", "total_sales", qty * price)
					p.hincrby("sales_summary", "total_tickets_sold", qty)
					p.hincrbyfloat("sales_summary", "total_sales:" + ticket_tiers[k], qty * price)
					p.hincrby("sales_summary", "total_tickets_sold:" + ticket_tiers[k], qty)
					p.execute()
					break

create_orders(250)



