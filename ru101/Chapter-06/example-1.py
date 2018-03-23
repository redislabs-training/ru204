from redis import StrictRedis, WatchError
import os
import time
import random
import string
import json
from datetime import date

redis = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"), 
                    port=os.environ.get("REDIS_PORT", 6379),
                    db=0)
redis.flushall()

# Part One - Check availability and Purchase
def generate_order_id():
  return ''.join(random.choice(string.ascii_uppercase + string.digits) \
    for _ in range(6))

def create_event(event_name, available, price):
  p = redis.pipeline()
  p.hsetnx("events:" + event_name, "capacity", available)
  p.hsetnx("events:" + event_name, "available", available)
  p.hsetnx("events:" + event_name, "price", price)
  p.execute()

def check_availability_and_purchase(user, event_name, qty):
  p = redis.pipeline()
  try:
    redis.watch("events:" + event_name)
    available = int(redis.hget("events:" + event_name, "available"))
    if available >= qty:
      order_id = generate_order_id()
      price = float(redis.hget("events:" + event_name, "price"))
      purchase = { 'who': user, 'qty': qty, 'ts': long(time.time()), 
                   'cost': qty * price, 'order_id': order_id }
      p.hincrby("events:" + event_name, "available", qty * -1)
      p.lpush("orders:" + event_name, json.dumps(purchase))
      p.execute()
  except WatchError:
    print "Write Conflict: {}".format("events:" + event_name)
  finally:
    p.reset()

# Check availability before purchasing
requestor = "Fred"
for_event = "Womens 4x400m Final"
create_event(for_event, 10, 9)
# Purchase, enough stock
check_availability_and_purchase(requestor, for_event, 5)
print redis.lrange("orders:" + for_event, 0, -1)
print redis.hgetall("events:" + for_event)

# No purchase, not enough stock
check_availability_and_purchase(requestor, for_event, 6)
print redis.lrange("orders:" + for_event, 0, -1)
print redis.hgetall("events:" + for_event)

# Part Two - Reserve stock & Credit Card auth
def reserve(user, event_name, qty):
  p = redis.pipeline()
  try:
    redis.watch("events:" + event_name)
    available = int(redis.hget("events:" + event_name, "available"))
    if available >= qty:
      order_id = generate_order_id()
      price = float(redis.hget("events:" + event_name, "price"))
      p.hincrby("events:" + event_name, "available", qty * -1)
      p.hincrby("events:" + event_name, "reservations", qty)
      p.hsetnx("events:" + event_name, "reservations-user:" + user, qty)
      p.hsetnx("events:" + event_name, "reservations-ts:" + user, long(time.time()))
      p.execute()
  except WatchError:
    print "Write Conflict: {}".format("events:" + event_name)
  finally:
    p.reset()
  if creditcard_auth(user):
    try:
      purchase = { 'who': user, 'qty': qty, 'ts': long(time.time()), 
                   'cost': qty * price, 'order_id': order_id }
      redis.watch("events:" + event_name)
      p.hincrby("events:" + event_name, "reservations", qty * -1)
      p.hdel("events:" + event_name, "reservations-user:" + user)
      p.hdel("events:" + event_name, "reservations-ts:" + user)
      p.lpush("orders:" + event_name, json.dumps(purchase))
      p.execute()
    except WatchError:
      print "Write Conflict: {}".format("events:" + event_name)
    finally:
      p.reset()
  else:
    print "Auth failure on order {} for {}".format(order_id, user)
    backout_reservation(user, event_name, qty)

def creditcard_auth(user):
  # TODO: Credit card auth happens here, but lets randomly fail
  # return random.choice([True, False])
  return True

def backout_reservation(user, event_name, qty):
  p = redis.pipeline()
  try:
    redis.watch("events:" + event_name)
    p.hincrby("events:" + event_name, "available", qty)
    p.hincrby("events:" + event_name, "reservations", qty * -1)
    p.hdel("events:" + event_name, "reservations-user:" + user)
    p.hdel("events:" + event_name, "reservations-ts:" + user)
    p.execute()
  except:
    print "Write Conflict: {}".format("events:" + event_name)
  finally:
    p.reset()

# Query results
for_event = "Womens Marathon Final"
create_event(for_event, 500, 9)
reserve(requestor, for_event, 5)
print redis.lrange("orders:" + for_event, 0, -1)
print redis.hgetall("events:" + for_event)

# Part Three - Expire Reservation
def create_expired_reservation(event_name):
  p = redis.pipeline()
  p.hset("events:" + event_name, "available", 485)
  p.hset("events:" + event_name, "reservations", 15)
  p.hset("events:" + event_name, "reservations-user:Fred", 3)
  p.hset("events:" + event_name, "reservations-ts:Fred", long(time.time() - 16))
  p.hset("events:" + event_name, "reservations-user:Jim", 5)
  p.hset("events:" + event_name, "reservations-ts:Jim", long(time.time() - 22))
  p.hset("events:" + event_name, "reservations-user:Amy", 7)
  p.hset("events:" + event_name, "reservations-ts:Amy", long(time.time() - 30))
  p.execute()

def expire_reservation(event_name):
  cutoff_ts = long(time.time()-30)
  for i in redis.hscan_iter("events:" + event_name, match="reservations-ts:*"):
    if long(i[1]) < cutoff_ts:
      (_, user) = i[0].split(":")
      qty = int(redis.hget("events:" + event_name, "reservations-user:" + user))
      backout_reservation(user, event_name, qty)  

# Expire reservations
for_event = "Womens Javelin"
create_expired_reservation(for_event)
expiration = time.time() + 20
while True:
  expire_reservation(for_event)
  oustanding = redis.hmget("events:" + for_event, "reservations-user:Fred", "reservations-user:Jim", "reservations-user:Amy")
  availbale = redis.hget("events:" + for_event, "available")
  print "{}, Available:{}, Reservations:{}".format(for_event, availbale, oustanding)
  if time.time() > expiration:
    break
  else:
    time.sleep(1)

# Part Four - Posting purchases
def reserve_with_pending(user, event_name, qty):
  p = redis.pipeline()
  try:
    redis.watch("events:" + event_name)
    available = int(redis.hget("events:" + event_name, "available"))
    if available >= qty:
      order_id = generate_order_id()
      price = float(redis.hget("events:" + event_name, "price"))
      p.hincrby("events:" + event_name, "available", qty * -1)
      p.hincrby("events:" + event_name, "reservations", qty)
      p.hsetnx("events:" + event_name, "reservations-user:" + user, qty)
      p.hsetnx("events:" + event_name, "reservations-ts:" + user, long(time.time()))
      p.execute()
  except WatchError:
    print "Write Conflict: {}".format("events:" + event_name)
  finally:
    p.reset()
  if creditcard_auth(user):
    try:
      purchase = { 'who': user, 'qty': qty, 'ts': long(time.time()), 'cost': qty * price, 
                   'order_id': order_id, 'event': event_name }
      redis.watch("events:" + event_name)
      p.hincrby("events:" + event_name, "reservations", qty * -1)
      p.hdel("events:" + event_name, "reservations-user:" + user)
      p.hdel("events:" + event_name, "reservations-ts:" + user)
      p.set("purchase_orders:" + order_id, json.dumps(purchase))
      p.lpush("pending:" + event_name, order_id)
      p.execute()
    except WatchError:
      print "Write Conflict: {}".format("events:" + event_name)
    finally:
      p.reset()
  else:
    print "Auth failure on order {} for {}".format(order_id, user)
    backout_reservation(user, event_name, qty)

def post_purchases(event_name):
  order_id = redis.rpop("pending:" + event_name)
  if order_id != None:
    p = redis.pipeline()
    order = json.loads(redis.get("purchase_orders:" + order_id))
    p.sadd("invoices:" + order['who'], order_id)
    p.sadd("sales:" + event_name, order_id)
    p.hincrbyfloat("sales_summary", event_name + ":total_sales", order['cost'])
    p.hincrby("sales_summary", event_name + ":total_tickets_sold", order['qty'])
    hour_of_day = int(time.strftime("%H"))
    vals = ["INCRBY", "u8", (hour_of_day+1) * 8, order['qty']]
    p.execute_command("BITFIELD", "sales_histogram:time_of_day", *vals)
    p.execute_command("BITFIELD", "sales_histogram:time_of_day:" + event_name, *vals)
    p.execute()

# Post purchases and query results
events = [
            { 'event': "Mens Discus", 'qty': 200, 'price': 10, 
              'buys' : [ { 'who': "Fred", 'required': 5 }, { 'who': "Amy", 'required': 2 } ] }, 
            { 'event': "Womens Discus", 'qty': 500, 'price': 15, 
              'buys': [ { 'who': "Jim", 'required': 20 }, { 'who': "Amy", 'required': 17 } ] }
          ]

for next_event in events:
  create_event(next_event['event'], next_event['qty'], next_event['price'])
  for buy in next_event['buys']:
    reserve_with_pending(buy['who'], next_event['event'], buy['required'])
    post_purchases(next_event['event'])

for next_event in events:
  print "=== Event: {}".format(next_event['event'])
  print "Details: {}".format(redis.hgetall("events:" + next_event['event']))
  print "Sales: {}".format(redis.smembers("sales:" + next_event['event']))
  for buy in next_event['buys']:
    print "Invoices for {}: {}".format(buy['who'], redis.smembers("invoices:" + buy['who']))

print "=== Orders"
for i in redis.scan_iter(match="purchase_orders:*"):
  print redis.get(i)  

print "=== Sales Summary \n{}".format(redis.hgetall("sales_summary"))

print "=== Sales Summary - hour of sale histogram"
hist = redis.get("sales_histogram:time_of_day")
for i in range(0, 24):
  vals = ["GET", "u8", (i+1) * 8]
  total_sales = int(redis.execute_command("BITFIELD", "sales_histogram:time_of_day", *vals)[0])
  print " {} = {}".format(i, total_sales)


