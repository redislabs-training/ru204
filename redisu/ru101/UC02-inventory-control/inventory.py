from redis import StrictRedis, WatchError
import os
import time
import random
import string
import json
from datetime import date
from sets import Set
import redisu.utils.keynamehelper as keynamehelper
import redisu.ru101.common.generate as generate

redis = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"), 
                    port=os.environ.get("REDIS_PORT", 6379),
                    db=0)

keynamehelper.set_prefix("uc02")

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
  c_set_key = keynamehelper.create_key_name("customers")
  for c in customers:
    c_key = keynamehelper.create_key_name("customer", c['id'])
    redis.hmset(c_key, c)
    redis.sadd(c_set_key, c['id'])

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
  e_set_key = keynamehelper.create_key_name("events")
  for e in events:
    # Override the availbaility & price if provided
    if available != None:
      e['available:' + tier] = available
    if price != None:
      e['price:' + tier] = price
    e_key = keynamehelper.create_key_name("event", e['sku'])
    redis.hmset(e_key, e)
    redis.sadd(e_set_key, e['sku'])

# Part One - Check availability and Purchase
def check_availability_and_purchase(customer, event_sku, qty, tier="General"):
  p = redis.pipeline()
  try:
    e_key = keynamehelper.create_key_name("event", event_sku)
    redis.watch(e_key)
    available = int(redis.hget(e_key, "available:" + tier))
    if available >= qty:
      order_id = generate.order_id()
      price = float(redis.hget(e_key, "price:" + tier))
      purchase = {  'order_id': order_id, 'customer': customer, 
                    'tier': tier, 'qty': qty, 'cost': qty * price, 'event_sku': event_sku,
                    'ts': long(time.time())}
      p.hincrby(e_key, "available:" + tier, -qty)
      so_key = keynamehelper.create_key_name("sales_order", order_id)
      p.hmset(so_key, purchase)
      p.execute()
  except WatchError:
    print "Write Conflict: {}".format(e_key)
  finally:
    p.reset()

def print_event_details(event_sku):
  e_key = keynamehelper.create_key_name("event", event_sku)
  print redis.hgetall(e_key)

# Create events with 10 tickets available
create_events(events, available=10)

# Stock availbale
requestor = "bill"
event_requested = "123-ABC-723"
check_availability_and_purchase(requestor, event_requested, 5)
print_event_details(event_requested)

# No purchase, not enough stock
requestor = "mary"
event_requested = "123-ABC-723"
check_availability_and_purchase(requestor, event_requested, 6)
print_event_details(event_requested)

# Part Two - Reserve stock & Credit Card auth
def reserve(customer, event_sku, qty, tier="General"):
  p = redis.pipeline()
  try:
    e_key = keynamehelper.create_key_name("event", event_sku)
    redis.watch(e_key)
    available = int(redis.hget(e_key, "available:" + tier))
    if available >= qty:
      order_id = generate.order_id()
      ts = long(time.time())
      price = float(redis.hget(e_key, "price:" + tier))
      p.hincrby(e_key, "available:" + tier, -qty)
      p.hsetnx(e_key, "hold-qty:" + order_id, qty)
      p.hsetnx(e_key, "hold-tier:" + order_id, tier)
      p.hsetnx(e_key, "hold-ts:" + order_id, ts)
      p.hincrby(e_key, "total-holds", qty)
      p.execute()
  except WatchError:
    print "Write Conflict in reserve: {}".format(e_key)
  finally:
    p.reset()
  if creditcard_auth(customer, qty * price):
    try:
      purchase = {  'order_id': order_id, 'customer': customer,
                    'tier': tier, 'qty': qty, 'cost': qty * price,  'event_sku': event_sku,
                    'ts': long(time.time()) }
      redis.watch(e_key)
      # Update the Event
      p.hdel(e_key, "hold-qty:" + order_id)
      p.hdel(e_key, "hold-tier:" + order_id)
      p.hdel(e_key, "hold-ts:" + order_id)
      p.hincrby(e_key, "total-holds", -qty)
      # Post the Sales Order
      so_key = keynamehelper.create_key_name("sales_order", order_id)
      p.hmset(so_key, purchase)
      p.execute()
    except WatchError:
      print "Write Conflict in reserve: {}".format(e_key)
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

def backout_hold(event_sku, order_id):
  p = redis.pipeline()
  try:
    e_key = keynamehelper.create_key_name("event", event_sku)
    redis.watch(e_key)
    qty = long(redis.hget(e_key, "hold-qty:" + order_id))
    tier = redis.hget(e_key, "hold-tier:" + order_id)
    p.hincrby(e_key, "available:" + tier, qty)
    p.hdel(e_key, "hold-qty:" + order_id)
    p.hdel(e_key, "hold-tier:" + order_id)
    p.hdel(e_key, "hold-ts:" + order_id)
    p.hincrby(e_key, "total-holds", -qty)
    p.execute()
  except WatchError:
    print "Write Conflict in backout_hold: {}".format(e_key)
  finally:
    p.reset()

# Create events with 10 tickets available
create_events(events, available=10)

# Make purchase with reservation and credit authorization steps
requestor = "jamie"
event_requested = "737-DEF-911"
reserve(requestor, event_requested, 5)
print_event_details(event_requested)

# Credit Auth failure for Joan
requestor = "joan"
event_requested = "737-DEF-911"
reserve(requestor, event_requested, 5)
print_event_details(event_requested)

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
  e_key = keynamehelper.create_key_name("event", event_sku)
  redis.hmset(e_key, attrs)

def expire_reservation(event_sku, cutoff_time_secs=30):
  cutoff_ts = long(time.time()-cutoff_time_secs)
  e_key = keynamehelper.create_key_name("event", event_sku)
  for field in redis.hscan_iter(e_key, match="hold-ts:*"):
    if long(field[1]) < cutoff_ts:
      (_, order_id) = field[0].split(":")
      backout_hold(event_sku, order_id)  

# Create events
create_events(events)

# Create expired reservations for the Event
event_requested = "320-GHI-921"
create_expired_reservation(event_requested)

tier = "General"
e_key = keynamehelper.create_key_name("event", event_requested)
while True:
  expire_reservation(event_requested)
  oustanding = redis.hmget(e_key, "hold-qty:VPIR6X", "hold-qty:B1BFG7", "hold-qty:UZ1EL0")
  availbale = redis.hget(e_key, "available:" + tier)
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
    e_key = keynamehelper.create_key_name("event", event_sku)
    redis.watch(e_key)
    available = int(redis.hget(e_key, "available:" + tier))
    if available >= qty:
      order_id = generate.order_id()
      ts = long(time.time())
      price = float(redis.hget(e_key, "price:" + tier))
      p.hincrby(e_key, "available:" + tier, -qty)
      p.hincrby(e_key, "total-holds", qty)
      p.hsetnx(e_key, "hold-qty:" + order_id, qty)
      p.hsetnx(e_key, "hold-tier:" + order_id, tier)
      p.hsetnx(e_key, "hold-ts:" + order_id, ts)
      p.execute()
  except WatchError:
    print "Write Conflict: {}".format("event:" + event_sku)
  finally:
    p.reset()
  if creditcard_auth(customer, qty * price):
    try:
      redis.watch(e_key)
      purchase = {  'order_id': order_id, 'customer': customer,  
                    'tier': tier, 'qty': qty, 'cost': qty * price, 'event': event_sku,
                    'ts': long(time.time()) }
      p.hincrby(e_key, "total-holds", -qty)
      p.hdel(e_key, "hold-qty:" + order_id)
      p.hdel(e_key, "hold-tier:" + order_id)
      p.hdel(e_key, "hold-ts:" + order_id)
      so_key = keynamehelper.create_key_name("sales_order", order_id)
      p.hmset(so_key, purchase)
      pending_set_key = keynamehelper.create_key_name("pending", event_sku)
      p.lpush(pending_set_key, order_id)
      p.execute()
    except WatchError:
      print "Write Conflict: {}".format("event:" + event_sku)
    finally:
      p.reset()
  else:
    print "Auth failure on order {} for customer {} ${}".format(order_id, customer, price * qty)
    backout_hold(event_sku, order_id)

def post_purchases(event_sku):
  pending_set_key = keynamehelper.create_key_name("pending", event_sku)
  order_id = redis.rpop(pending_set_key)
  if order_id != None:
    try:
      p = redis.pipeline()
      so_key = keynamehelper.create_key_name("sales_order", order_id)
      customer, cost, qty = redis.hmget(so_key, "customer", "cost", "qty")
      e_key = keynamehelper.create_key_name("event", event_sku)
      event_name = redis.hget(e_key, "name")
      so_set_key = keynamehelper.create_key_name("sales_orders", event_sku)
      p.sadd(so_set_key, order_id)
      i_set_key = keynamehelper.create_key_name("invoices", customer)
      p.sadd(i_set_key, order_id)
      sum_key = keynamehelper.create_key_name("sales_summary")
      p.hincrbyfloat(sum_key, "total_sales:" + event_name, cost)
      p.hincrby(sum_key, "total_tickets_sold:" + event_name, qty)
      p.hincrbyfloat(sum_key, "total_sales", cost)
      p.hincrby(sum_key, "total_tickets_sold", qty)
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

e_set_key = keynamehelper.create_key_name("events")
for sku in redis.sscan_iter(e_set_key):
  print "= Event: {}".format(sku)
  e_key = keynamehelper.create_key_name("event", sku)
  print " Details: {}".format(redis.hgetall(e_key))
  print " + Sales Orders: ",
  so_set_key = keynamehelper.create_key_name("sales_orders", sku)
  for so in redis.sscan_iter(so_set_key):
    print so,
  print "\n"

c_set_key = keynamehelper.create_key_name("customers")
for c in redis.sscan_iter(c_set_key):
  c_key = keynamehelper.create_key_name("customer", c)
  customer_name = redis.hget(c_key, "customer_name")
  print "= Customer: {}".format(customer_name)
  inv_set_key = keynamehelper.create_key_name("invoices", c)
  for k in redis.sscan_iter(inv_set_key):
    print " + Invoice: {}".format(k)
    so_key = keynamehelper.create_key_name("sales_order", k)
    print "   + Details: {}".format(redis.hgetall(so_key))

sum_key = keynamehelper.create_key_name("sales_summary")
print "= Sales Summary \n{}".format(redis.hgetall(sum_key))

