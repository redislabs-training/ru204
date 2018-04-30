from redis import StrictRedis, WatchError
import os
import time
import random
import string
import json
from datetime import date
import redisu.ru101.common

redis = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"), 
                    port=os.environ.get("REDIS_PORT", 6379),
                    db=0)

chapter_prefix = "uc02:"

customers = [
  { 'id': "bill", 'customer_name': "bill smith"},
  { 'id': "mary", 'customer_name': "mary jane"},
  { 'id': "jamie", 'customer_name': "jamie north"},
  { 'id': "joan", 'customer_name': 'joan west'},
  { 'id': "fred", 'customer_name': "fred smith"},
  { 'id': "amy", 'customer_name': 'amy south'},
  { 'id': "jim", 'customer_name': 'jim somebody'}
]

def create_customers(customers):
  for c in customers:
    redis.hmset(chapter_prefix + "customer:" + c['id'], c)
    redis.sadd(chapter_prefix + "customers", c['id'])

create_customers(customers)

events = [
  { 'sku': "123-ABC-723",
    'name': "Men's 100m Final",
    'disabled_access': True,
    'medal_event': True,
    'venue': "Olympic Stadium",
    'category': "Track & Field",
    'capacity': 60102,
    'available:General': 20000,
    'price:General': 25.00
  },
  { 'sku': "737-DEF-911",
    'name': "Women's 4x100m Heats",
    'disabled_access': True,
    'medal_event': False,
    'venue': "Olympic Stadium",
    'category': "Track & Field",
    'capacity': 60102,
    'available:General': 10000,
    'price:General': 19.50
  },
  { 'sku': "320-GHI-921",
    'name': "Womens Judo Qualifying",
    'disabled_access': False,
    'medal_event': False,
    'venue': "Nippon Budokan",
    'category': "Martial Arts",
    'capacity': 14471,
    'available:General': 5000,
    'price:General': 15.25  
  }      
]

def create_events(events, available=None, price=None, tier="General"):
  redis.delete(chapter_prefix + "events")
  for e in events:
    # Override the availbaility & price if provided
    if available != None:
      e['available:' + tier] = available
    if price != None:
      e['price:' + tier] = price
    redis.delete(chapter_prefix + "event:" + e['sku'])
    redis.hmset(chapter_prefix + "event:" + e['sku'], e)
    redis.sadd(chapter_prefix + "events", e['sku'])

# Part One - Check availability and Purchase
def check_availability_and_purchase(customer, event_sku, qty, tier="General"):
  p = redis.pipeline()
  try:
    redis.watch(chapter_prefix + "event:" + event_sku)
    available = int(redis.hget(chapter_prefix + "event:" + event_sku, "available:" + tier))
    if available >= qty:
      order_id = redisu.ru101.common.generate.order_id()
      price = float(redis.hget(chapter_prefix + "event:" + event_sku, "price:" + tier))
      purchase = {  'order_id': order_id, 'customer': customer, 
                    'tier': tier, 'qty': qty, 'cost': qty * price, 'event_sku': event_sku,
                    'ts': long(time.time())}
      p.hincrby(chapter_prefix + "event:" + event_sku, "available:" + tier, -qty)
      p.hmset(chapter_prefix + "sales_order:" + order_id, purchase)
      p.execute()
  except WatchError:
    print "Write Conflict: {}".format("events:" + event_name)
  finally:
    p.reset()

# Create events with 10 tickets available
create_events(events, available=10)

# Stock availbale
requestor = "bill"
event_requested = "123-ABC-723"
check_availability_and_purchase(requestor, event_requested, 5)

print redis.hgetall(chapter_prefix + "event:" + event_requested)

# No purchase, not enough stock
requestor = "mary"
event_requested = "123-ABC-723"
check_availability_and_purchase(requestor, event_requested, 6)

print redis.hgetall(chapter_prefix + "event:" + event_requested)

# Part Two - Reserve stock & Credit Card auth
def reserve(customer, event_sku, qty, tier="General"):
  p = redis.pipeline()
  try:
    key_name = chapter_prefix + "event:" + event_sku
    redis.watch(key_name)
    available = int(redis.hget(key_name, "available:" + tier))
    if available >= qty:
      order_id = redisu.ru101.commongenerate_order_id()
      ts = long(time.time())
      price = float(redis.hget(key_name, "price:" + tier))
      p.hincrby(key_name, "available:" + tier, -qty)
      p.hsetnx(key_name, "hold-qty:" + order_id, qty)
      p.hsetnx(key_name, "hold-tier:" + order_id, tier)
      p.hsetnx(key_name "hold-ts:" + order_id, ts)
      p.hincrby(key_name, "total-holds", qty)
      p.execute()
  except WatchError:
    print "Write Conflict: {}".format("event:" + event_sku)
  finally:
    p.reset()
  if creditcard_auth(customer, qty * price):
    try:
      purchase = {  'order_id': order_id, 'customer': customer,
                    'tier': tier, 'qty': qty, 'cost': qty * price,  'event_sku': event_sku,
                    'ts': long(time.time()) }
      redis.watch(key_name)
      # Update the Event
      p.hdel(key_name, "hold-qty:" + order_id)
      p.hdel(key_name, "hold-tier:" + order_id)
      p.hdel(key_name, "hold-ts:" + order_id)
      p.hincrby(key_name, "total-holds", -qty)
      # Post the Sales Order
      p.hmset(chapter_prefix + "sales_order:" + order_id, purchase)
      p.execute()
    except WatchError:
      print "Write Conflict: {}".format("events:" + event_name)
    finally:
      p.reset()
  else:
    print "Auth failure on order {} for customer {} ${}".format(order_id, customer, price * qty)
    backout_hold(event_sku, order_id)

def creditcard_auth(customer, order_total):
  # Always fails Joan's auth
  if customer.upper() == "JOAN":
    return False
  else:
    return True

def creditcard_auth_ask(customer, order_total):
  # # Randomly approve or denigh credit card auth
  # return random.choice([True, False])
  resp = raw_input("Auth customer '{}'' for ${} [Yes|No]? ".format(customer, order_total))
  if resp.upper() == "NO":
    return False
  else:
    return True

def creditcard_auth_random(customer, order_total):
  # Randomly approve or denigh credit card auth
  return random.choice([True, False])

def backout_hold(event_sku, order_id):
  p = redis.pipeline()
  try:
    key_name = chapter_prefix + "event:" + event_sku
    redis.watch(key_name)
    qty = long(redis.hget(key_name, "hold-qty:" + order_id))
    p.hincrby(key_name, "available:" + tier, qty)
    p.hdel(key_name, "hold-qty:" + order_id)
    p.hdel(key_name, "hold-tier:" + order_id)
    p.hdel(key_name, "hold-ts:" + order_id)
    p.hincrby(key_name, "total-holds", -qty)
    p.execute()
  except:
    print "Write Conflict: {}".format("event:" + event_sku)
  finally:
    p.reset()

# Create events with 10 tickets available
create_events(events, available=10)

# Make purchase with reservation and credit authorization steps
requestor = "jamie"
event_requested = "737-DEF-911"
reserve(requestor, event_requested, 5)

print redis.hgetall(chapter_prefix + "event:" + event_requested)

# Credit Auth failure for Joan
requestor = "joan"
event_requested = "737-DEF-911"
reserve(requestor, event_requested, 5)

print redis.hgetall(chapter_prefix + "event:" + event_requested)

# Part Three - Expire Reservation
def create_expired_reservation(event_sku, tier="General"):
  attrs = { 'available:' + tier: 485,
            'total-holds': 15,
            'hold-qty:VPIR6X': 3,            
            'hold-tier:VPIR6X': "General",
            'hold-ts:VPIR6X': long(time.time() - 16),
            'hold-qty:B1BFG7': 5,
            'hold-tier:B1BFG7': "General",
            'hold-ts:B1BFG7': long(time.time() - 22),
            'hold-qty:UZ1EL0': 7,
            'hold-tier:UZ1EL0': "General",
            'hold-ts:UZ1EL0': long(time.time() - 30)
          }
  redis.hmset(chapter_prefix + "event:" + event_sku, attrs)

def expire_reservation(event_sku, cutoff_time_secs=30):
  cutoff_ts = long(time.time()-cutoff_time_secs)
  for field in redis.hscan_iter(chapter_prefix + "event:" + event_sku, match="hold-ts:*"):
    if long(field[1]) < cutoff_ts:
      (_, order_id) = field[0].split(":")
      backout_hold(event_sku, order_id)  

# Create events
create_events(events)

# Create expired reservations for the Event
event_requested = "320-GHI-921"
create_expired_reservation(event_requested)

tier = "General"
while True:
  expire_reservation(event_requested)
  oustanding = redis.hmget(chapter_prefix + "event:" + event_requested, "hold-qty:VPIR6X", "hold-qty:B1BFG7", "hold-qty:UZ1EL0")
  availbale = redis.hget(chapter_prefix + "event:" + event_requested, "available:" + tier)
  print "{}, Available:{}, Reservations:{}".format(event_requested, availbale, oustanding)
  # Break if all items in oustanding list are None
  if all(v is None for v in oustanding):
    break
  else:
    time.sleep(1)

# Part Four - Posting purchases
def reserve_with_pending(customer, event_sku, qty, tier="General"):
  p = redis.pipeline()
  try:
    key_name = chapter_prefix + "event:" + event_sku
    redis.watch(key_name)
    available = int(redis.hget(key_name, "available:" + tier))
    if available >= qty:
      order_id = redisu.ru101.common.generate.order_id()
      ts = long(time.time())
      price = float(redis.hget(key_name, "price:" + tier))
      p.hincrby(key_name, "available:" + tier, -qty)
      p.hincrby(key_name, "total-holds", qty)
      p.hsetnx(key_name, "hold-qty:" + order_id, qty)
      p.hsetnx(key_name, "hold-tier:" + order_id, tier)
      p.hsetnx(key_name, "hold-ts:" + order_id, ts)
      p.execute()
  except WatchError:
    print "Write Conflict: {}".format("event:" + event_sku)
  finally:
    p.reset()
  if creditcard_auth(customer, qty * price):
    try:
      redis.watch(key_name)
      purchase = {  'order_id': order_id, 'customer': customer,  
                    'tier': tier, 'qty': qty, 'cost': qty * price, 'event': event_sku,
                    'ts': long(time.time()) }
      p.hincrby(key_name, "total-holds", -qty)
      p.hdel(key_name, "hold-qty:" + order_id)
      p.hdel(key_name, "hold-tier:" + order_id)
      p.hdel(key_name, "hold-ts:" + order_id)
      p.hmset(chapter_prefix + "sales_order:" + order_id, purchase)
      p.lpush(chapter_prefix + "pending:" + event_sku, order_id)
      p.execute()
    except WatchError:
      print "Write Conflict: {}".format("event:" + event_sku)
    finally:
      p.reset()
  else:
    print "Auth failure on order {} for customer {} ${}".format(order_id, customer, price * qty)
    backout_hold(event_sku, order_id)

def post_purchases(event_sku):
  order_id = redis.rpop(chapter_prefix + "pending:" + event_sku)
  if order_id != None:
    try:
      p = redis.pipeline()
      customer, cost, qty = redis.hmget(chapter_prefix + "sales_order:" + order_id, "customer", "cost", "qty")
      event_name = redis.hget(chapter_prefix + "event:" + event_sku, "name")
      p.sadd(chapter_prefix + "sales_orders:" + event_sku , order_id)
      p.sadd(chapter_prefix + "invoices:" + customer, order_id)
      p.hincrbyfloat(chapter_prefix + "sales_summary", "total_sales:" + event_name, cost)
      p.hincrby(chapter_prefix + "sales_summary", "total_tickets_sold:" + event_name, qty)
      p.hincrbyfloat(chapter_prefix + "sales_summary", "total_sales", cost)
      p.hincrby(chapter_prefix + "sales_summary", "total_tickets_sold", qty)
      p.execute()
    finally:
      p.reset()

# Post purchases and query results
purchases = [
              { 'customer': "fred",
                'buys': [ { 'sku': "123-ABC-723", 'required': 5 } ]
              },
              { 'customer': "amy",
                'buys': [ { 'sku': "123-ABC-723", 'required': 2 }, { 'sku': "737-DEF-911", 'required': 17 } ]
              },
              { 'customer': "jim",
                'buys': [ { 'sku': "737-DEF-911", 'required': 20 } ]
              }
            ]

create_events(events, available=200, price=15)
products_purchased = Set()
for customer in purchases:
  for purchase in customer['buys']:
    reserve_with_pending(customer['customer'], purchase['sku'], purchase['required'])
    post_purchases(purchase['sku'])

for sku in redis.sscan_iter(chapter_prefix + "events"):
  print "= Event: {}".format(sku)
  print " Details: {}".format(redis.hgetall(chapter_prefix + "event:" + sku))
  print " + Sales Orders: ",
  for so in redis.sscan_iter(chapter_prefix + "sales_orders:" + sku):
    print so,
  print "\n"

for c in redis.sscan_iter(chapter_prefix + "customers"):
  customer_name = redis.hget(chapter_prefix + "customer:" + c, "customer_name")
  print "= Customer: {}".format(customer_name)
  for k in redis.sscan_iter(chapter_prefix + "invoices:" + c):
    print " + Invoice: {}".format(k)
    print "   + Details: {}".format(redis.hgetall(chapter_prefix + "sales_order:" + k))

print "= Sales Summary \n{}".format(redis.hgetall(chapter_prefix + "sales_summary"))

