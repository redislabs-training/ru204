from redis import StrictRedis, WatchError
import os
import time
import random
import string
import json
from datetime import date
from sets import Set

redis = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"), 
                    port=os.environ.get("REDIS_PORT", 6379),
                    db=0)

chapter_prefix = "ch06:"

events = [
  { 'sku': "123-ABC-723",
    'name': "Men's 100m Final",
    'disabled_access': True,
    'medal_event': True,
    'venue': "Olympic Stadium",
    'category': "Track & Field",
    'capacity': 60102,
    'available': 20000,
    'price': 25.00
  },
  { 'sku': "737-DEF-911",
    'name': "Women's 4x100m Heats",
    'disabled_access': True,
    'medal_event': False,
    'venue': "Olympic Stadium",
    'category': "Track & Field",
    'capacity': 60102,
    'available': 10000,
    'price': 19.50
  },
  { 'sku': "320-GHI-921",
    'name': "Womens Judo Qualifying",
    'disabled_access': False,
    'medal_event': False,
    'venue': "Nippon Budokan",
    'category': "Martial Arts",
    'capacity': 14471,
    'available': 5000,
    'price': 15.25  
  }      
]

def create_events(events, available=None, price=None):
  for e in events:
    # Override the availbaility & price if provided
    if available != None:
      e['available'] = available
    if price != None:
      e['price'] = price
    redis.delete(chapter_prefix + "event:" + e['sku'])
    redis.hmset(chapter_prefix + "event:" + e['sku'], e)

# Part One - Check availability and Purchase
def generate_order_id():
  return ''.join(random.choice(string.ascii_uppercase + string.digits) \
    for _ in range(6))

def check_availability_and_purchase(user, event_sku, qty):
  p = redis.pipeline()
  try:
    redis.watch(chapter_prefix + "event:" + event_sku)
    available = int(redis.hget(chapter_prefix + "event:" + event_sku, "available"))
    if available >= qty:
      order_id = generate_order_id()
      price = float(redis.hget(chapter_prefix + "event:" + event_sku, "price"))
      purchase = { 'who': user, 'qty': qty, 'ts': long(time.time()), 
                   'cost': qty * price, 'order_id': order_id }
      p.hincrby(chapter_prefix + "event:" + event_sku, "available", qty * -1)
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

print redis.lrange(chapter_prefix + "sales_orders:" + event_requested, 0, -1)
print redis.hgetall(chapter_prefix + "event:" + event_requested)

# No purchase, not enough stock
requestor = "mary"
event_requested = "123-ABC-723"
check_availability_and_purchase(requestor, event_requested, 6)

print redis.lrange(chapter_prefix + "sales_orders:" + event_requested, 0, -1)
print redis.hgetall(chapter_prefix + "event:" + event_requested)

# Part Two - Reserve stock & Credit Card auth
def reserve(user, event_sku, qty):
  p = redis.pipeline()
  try:
    redis.watch(chapter_prefix + "event:" + event_sku)
    available = int(redis.hget(chapter_prefix + "event:" + event_sku, "available"))
    if available >= qty:
      order_id = generate_order_id()
      ts = long(time.time())
      price = float(redis.hget(chapter_prefix + "event:" + event_sku, "price"))
      p.hincrby(chapter_prefix + "event:" + event_sku, "available", qty * -1)
      p.hsetnx(chapter_prefix + "event:" + event_sku, "hold-qty:" + order_id, qty)
      p.hsetnx(chapter_prefix + "event:" + event_sku, "hold-ts:" + order_id, ts)
      p.hincrby(chapter_prefix + "event:" + event_sku, "total-holds", qty)
      p.execute()
  except WatchError:
    print "Write Conflict: {}".format("event:" + event_sku)
  finally:
    p.reset()
  if creditcard_auth(user, qty * price):
    try:
      purchase = { 'who': user, 'qty': qty, 'ts': long(time.time()), 
                   'cost': qty * price, 'order_id': order_id, 'sku': event_sku }
      redis.watch(chapter_prefix + "event:" + event_sku)
      p.hdel(chapter_prefix + "event:" + event_sku, "hold-qty:" + order_id)
      p.hdel(chapter_prefix + "event:" + event_sku, "hold-ts:" + order_id)
      p.hincrby(chapter_prefix + "event:" + event_sku, "total-holds", qty * -1)
      p.hmset(chapter_prefix + "sales_order:" + order_id, purchase)
      p.execute()
    except WatchError:
      print "Write Conflict: {}".format("events:" + event_name)
    finally:
      p.reset()
  else:
    print "Auth failure on order {} for customer {} ${}".format(order_id, user, price * qty)
    backout_hold(event_sku, order_id)

def creditcard_auth(user, order_total):
  # Always fails Joan's auth
  if user.upper() == "JOAN":
    return False
  else:
    return True

def creditcard_auth_ask(user, order_total):
  # # Randomly approve or denigh credit card auth
  # return random.choice([True, False])
  resp = raw_input("Auth customer '{}'' for ${} [Yes|No]? ".format(user, order_total))
  if resp.upper() == "NO":
    return False
  else:
    return True

def creditcard_auth_random(user, order_total):
  # Randomly approve or denigh credit card auth
  return random.choice([True, False])

def backout_hold(event_sku, order_id):
  p = redis.pipeline()
  try:
    redis.watch(chapter_prefix + "event:" + event_sku)
    qty = long(redis.hget(chapter_prefix + "event:" + event_sku, "hold-qty:" + order_id))
    p.hincrby(chapter_prefix + "event:" + event_sku, "available", qty)
    p.hdel(chapter_prefix + "event:" + event_sku, "hold-qty:" + order_id)
    p.hdel(chapter_prefix + "event:" + event_sku, "hold-ts:" + order_id)
    p.hincrby(chapter_prefix + "event:" + event_sku, "total-holds", qty * -1)
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

requestor = "joan"
event_requested = "737-DEF-911"
reserve(requestor, event_requested, 5)

print redis.hgetall(chapter_prefix + "event:" + event_requested)

# Part Three - Expire Reservation
def create_expired_reservation(event_sku):
  attrs = { 'available': 485,
            'total-holds': 15,
            'hold-qty:VPIR6X': 3,
            'hold-ts:VPIR6X': long(time.time() - 16),
            'hold-qty:B1BFG7': 5,
            'hold-ts:B1BFG7': long(time.time() - 22),
            'hold-qty:UZ1EL0': 7,
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

while True:
  expire_reservation(event_requested)
  oustanding = redis.hmget(chapter_prefix + "event:" + event_requested, "hold-qty:VPIR6X", "hold-qty:B1BFG7", "hold-qty:UZ1EL0")
  availbale = redis.hget(chapter_prefix + "event:" + event_requested, "available")
  print "{}, Available:{}, Reservations:{}".format(event_requested, availbale, oustanding)
  # Break if all items in oustanding list are None
  if all(v is None for v in oustanding):
    break
  else:
    time.sleep(1)

# Part Four - Posting purchases
def reserve_with_pending(user, event_sku, qty):
  p = redis.pipeline()
  try:
    redis.watch(chapter_prefix + "event:" + event_sku)
    available = int(redis.hget(chapter_prefix + "event:" + event_sku, "available"))
    if available >= qty:
      order_id = generate_order_id()
      ts = long(time.time())
      price = float(redis.hget(chapter_prefix + "event:" + event_sku, "price"))
      p.hincrby(chapter_prefix + "event:" + event_sku, "available", qty * -1)
      p.hincrby(chapter_prefix + "event:" + event_sku, "total-holds", qty)
      p.hsetnx(chapter_prefix + "event:" + event_sku, "hold-qty:" + order_id, qty)
      p.hsetnx(chapter_prefix + "event:" + event_sku, "hold-ts:" + order_id, ts)
      p.execute()
  except WatchError:
    print "Write Conflict: {}".format("event:" + event_sku)
  finally:
    p.reset()
  if creditcard_auth(user, qty * price):
    try:
      purchase = { 'who': user, 'qty': qty, 'ts': long(time.time()), 'cost': qty * price, 
                   'order_id': order_id, 'event': event_sku }
      redis.watch(chapter_prefix + "event:" + event_sku)
      p.hincrby(chapter_prefix + "event:" + event_sku, "total-holds", qty * -1)
      p.hdel(chapter_prefix + "event:" + event_sku, "hold-qty:" + order_id)
      p.hdel(chapter_prefix + "event:" + event_sku, "hold-ts:" + order_id)
      p.hmset(chapter_prefix + "sales_order:" + order_id, purchase)
      p.lpush(chapter_prefix + "pending:" + event_sku, order_id)
      p.execute()
    except WatchError:
      print "Write Conflict: {}".format("event:" + event_sku)
    finally:
      p.reset()
  else:
    print "Auth failure on order {} for customer {} ${}".format(order_id, user, price * qty)
    backout_hold(event_sku, order_id)

def post_purchases(event_sku):
  order_id = redis.rpop(chapter_prefix + "pending:" + event_sku)
  if order_id != None:
    try:
      p = redis.pipeline()
      who, cost, qty = redis.hmget(chapter_prefix + "sales_order:" + order_id, "who", "cost", "qty")
      p.lpush(chapter_prefix + "sales_orders:" + event_sku, order_id)
      p.lpush(chapter_prefix + "invoices:" + who, order_id)
      p.hincrbyfloat(chapter_prefix + "sales_summary", "total_sales:" + event_sku, cost)
      p.hincrby(chapter_prefix + "sales_summary", "total_tickets_sold:" + event_sku, qty)
      p.hincrbyfloat(chapter_prefix + "sales_summary", "total_sales", cost)
      p.hincrby(chapter_prefix + "sales_summary", "total_tickets_sold", qty)
      p.execute()
    finally:
      p.reset()

# Post purchases and query results
purchases = [
              { 'who': "fred",
                'buys': [ { 'sku': "123-ABC-723", 'required': 5 } ]
              },
              { 'who': "amy",
                'buys': [ { 'sku': "123-ABC-723", 'required': 2 }, { 'sku': "737-DEF-911", 'required': 17 } ]
              },
              { 'who': "jim",
                'buys': [ { 'sku': "737-DEF-911", 'required': 20 } ]
              }
            ]

create_events(events, available=200, price=15)
products_purchased = Set()
for customer in purchases:
  for purchase in customer['buys']:
    reserve_with_pending(customer['who'], purchase['sku'], purchase['required'])
    post_purchases(purchase['sku'])
    products_purchased.add(purchase['sku'])

for sku in products_purchased:
  print "= Event: {}".format(sku)
  print " Details: {}".format(redis.hgetall(chapter_prefix + "event:" + sku))
  print " + Sales Orders: {}".format(redis.lrange(chapter_prefix + "sales_orders:" + sku, 0, -1)) 

for customer in purchases:
  print "= Customer: {}".format(customer['who'])
  # print " + Invoices for {}: {}".format(customer['who'], redis.smembers(chapter_prefix + "invoices:" + customer['who']))
  for k in redis.lrange(chapter_prefix + "invoices:" + customer['who'], 0, -1):
    print " + Invoice: {}".format(k)
    print "   + Details: {}".format(redis.hgetall(chapter_prefix + "sales_order:" + k))

print "= Sales Summary \n{}".format(redis.hgetall(chapter_prefix + "sales_summary"))

