from redis import StrictRedis
import os
import hashlib
import json
import random
from faker import Faker
import string
import math
import struct
import time
import redisu.utils.textincr as textincr
import redisu.ru101.common.generate

redis = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"), 
                    port=os.environ.get("REDIS_PORT", 6379),
                    db=0)

fake = Faker()
p = redis.pipeline()

customers = []
def create_customers(num):
  fake.seed(94002)
  for _ in range(num):
    id = redisu.ru101.common.generate.cust_id()
    p.hmset("customer:" + id, {'customer_name': fake.name(), 'address': fake.address(), 'phone': fake.phone_number()})
    p.sadd("customers", id)
    p.execute()
    customers.append(id)

create_customers(501)

ticket_tiers = ["Lottery", "General", "Reserved", "VIP"]

events = []
def create_event(event, venue, capacity=None, geo=None,
                 add_faceted_search=False, add_hashed_search=False, add_seatmap=False):
  sku = redisu.ru101.common.generate.sku()
  p.sadd("events", sku)
  p.sadd("event:skus:" + event, sku)
  p.sadd("venues:" + sku, venue)
  attrs = { 'name': event,
            'venue': venue, 
            'medal_event' : fake.random_element((True, False)),
            'disabled_access' : fake.random_element((True, False))}
  if capacity is not None:
    event_capacity = random.randint(capacity/10, capacity/2)
    attrs['capacity'] = event_capacity
    tiers_availbale = random.randint(1,3)
    tier_capacity = int(round(event_capacity / tiers_availbale))
    event_remaining = event_capacity
    for k in range(tiers_availbale, 0, -1):
      # tier_availability = random.randint(((event_capacity/tiers_availbale))/2, (event_capacity/tiers_availbale)) 
      # event_remaining = event_remaining - tier_availability
      # attrs['available:' + ticket_tiers[k]] = tier_availability if (k != 0 ) else event_remaining 
      attrs['available:' + ticket_tiers[k]] = tier_capacity
      attrs['price:' + ticket_tiers[k]] = random.randint(10 * (k+1), 10 * (k+1) + 9)
    p.hmset("event:" + sku, attrs)
    if add_seatmap:
      create_seatmap(sku, tiers_availbale, tier_capacity)
  attrs['sku'] = sku
  if geo is not None:
    p.geoadd("geo:event:" + event, geo['long'], geo['lat'], venue)
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

max_seats_per_block=32
def create_seatmap(event_sku, tiers, capacity):
  block_name = "A"
  # Use this formula if you want multiple 32bit blocks stored in a single key. More compact, harder to understand
  # seats_per_block = min(max_seats_per_block, -(-capacity / tiers))
  seats_per_block = max_seats_per_block
  blocks_to_fill = -(-capacity // seats_per_block)
  to_fill = capacity
  for k in range(blocks_to_fill):
    seats_in_block = min(to_fill, seats_per_block)
    filled_seat_map = int(math.pow(2, seats_in_block))-1
    # vals = ["SET", "u32", k * seats_per_block, filled_seat_map]
    vals = ["SET", "u32", 0, filled_seat_map]
    p.execute_command("BITFIELD", "seatmap:" + event_sku + ":" + ticket_tiers[(k % tiers) +1] + ":" + block_name, *vals)
    to_fill -= seats_in_block
    block_name = textincr.incr_str(block_name)
  p.execute()   

def create_transit(transit, venue, event_sku, geo=None):
    p.sadd("transit:" + transit + ":events", event_sku)
    if geo is not None:
      p.geoadd("geo:transit:" + transit, geo['long'], geo['lat'], venue)

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
        p.geoadd("geo:venues", v['geo']['long'], v['geo']['lat'], v['venue'])
    p.execute()

create_venues()

def create_orders(num_customers=100, max_orders_per_customer=20):
  for i in range(num_customers):
    num_orders = random.randint(1, max_orders_per_customer)
    customer_id = customers[random.randint(0, len(customers)-1)]
    customer_name = redis.hget("customer:" + customer_id, "customer_name")
    for j in range(num_orders):
      order_id = redisu.ru101.common.generate.order_id()
      event_sku = events[random.randint(0, len(events)-1)]
      for k in range(len(ticket_tiers)-1, 0, -1):
        if redis.hexists("event:" + event_sku, "available:" + ticket_tiers[k]):
          price = float(redis.hget("event:" + event_sku, "price:" + ticket_tiers[k]))
          availbale = long(redis.hget("event:" + event_sku, "available:" + ticket_tiers[k]))
          event_name = redis.hget("event:" + event_sku, "name")
          if availbale > 1:
            qty = random.randint(1, min(75,availbale/2))
          elif availbale == 1:
            qty = 1
          else:
            continue
          res = find_seats(event_sku, ticket_tiers[k], qty)
          ts = long(time.time())
          purchase = {  'customer': customer_id, 'customer_name': customer_name,
                        'order_id': order_id, 'event': event_sku, 'event_name': event_name,
                        'tier': ticket_tiers[k], 'qty': qty, 'cost': qty * price, 
                        'seats' : res['seats'],
                        'ts': ts }  
          p.hmset("sales_order:" + order_id, purchase)
          inv = { 'customer': customer_id,
                  'order_date': ts,
                  'due_date': ts + datetime.timedelta(days=90),
                  'amount_due': qty * price,
                  'status': "Invoiced" }
          p.hmset("invoice:" + order_id, inv)
          p.sadd("invoices:" + customer_id, order_id)
          p.hincrby("event:" + event_sku, "available:" + ticket_tiers[k], -qty)
          p.sadd("event:" + event_sku + ":sales_orders", order_id)
          p.sadd("invoices:" + customer_id, order_id)
          p.hincrbyfloat("sales_summary:" + event_name, "total_sales", qty * price)
          p.hincrby("sales_summary" + event_name, "total_tickets_sold", qty)
          p.hincrbyfloat("sales_summary:" + event_name, "total_sales:" + ticket_tiers[k], qty * price)
          p.hincrby("sales_summary:" + event_name, "total_tickets_sold:" + ticket_tiers[k], qty)
          p.hincrbyfloat("sales_summary", "total_sales", qty * price)
          p.hincrby("sales_summary", "total_tickets_sold", qty)
          p.hincrbyfloat("sales_summary", "total_sales:" + ticket_tiers[k], qty * price)
          p.hincrby("sales_summary", "total_tickets_sold:" + ticket_tiers[k], qty)
          p.execute()
          break

# def find_seats(event_sku, tier, qty):
#   # Find seat maps
#   allocated_seats = []
#   total_allocated = 0
#   to_allocate = qty
#   for key in redis.scan_iter("seatmap:" + event_sku + ":" + tier + ":*"):
#     available = redis.bitcount(key)
#     if available > 0:
#       block_name = key.split(":")[3]
#       vals = ["GET", "u32", 0]
#       new_seat_map = int(redis.execute_command("BITFIELD", key, *vals)[0])
#       first_seat = (new_seat_map&-new_seat_map).bit_length()-1
#       if to_allocate >= available:
#         # All seats required
#         new_seat_map = 0
#         taken = available
#       else:
#         # subtract needed seats
#         taken = to_allocate
#         for k in range(first_seat, first_seat + to_allocate):
#           new_seat_map -= int(math.pow(2, k))
#       vals = ["SET", "u32", 0, new_seat_map]
#       new_seat_map = redis.execute_command("BITFIELD", key, *vals)
#       allocated_seats.append(block_name + ":" + str(first_seat) + "-" + str(first_seat + taken-1))
#       total_allocated += taken
#       if (to_allocate <= available):
#         break
#       to_allocate -= taken
#   return { 'requested': qty, 'assigned': total_allocated, 'seats': allocated_seats }

def find_seats(event_sku, tier, qty):
  # Find seat maps
  allocated_seats = []
  total_allocated = 0
  to_allocate = qty
  for key in redis.scan_iter("seatmap:" + event_sku + ":" + tier + ":*"):
    available = redis.bitcount(key)
    if available > 0:
      vals = ["GET", "u32", 0]
      new_seat_map = int(redis.execute_command("BITFIELD", key, *vals)[0])
      # Take some seats from this block
      num_taking = max(1, min(available/2, to_allocate/2))
      pos = range(0,31)
      random.shuffle(pos)
      current_pos=0
      for i in range(num_taking):
        if ( new_seat_map >> pos[current_pos] & 1 ):
          new_seat_map -= int(math.pow(2, pos[current_pos]))
          vals = ["SET", "u32", 0, new_seat_map]
          redis.execute_command("BITFIELD", key, *vals)
          block_name = key.split(":")[3]
          allocated_seats.append(block_name + ":" + str(pos[current_pos]))
          current_pos += 1
          total_allocated += 1
          to_allocate -= 1
      if (to_allocate == 0):
        break
    if (to_allocate == 0):
      break
  return { 'requested': qty, 'assigned': total_allocated, 'seats': allocated_seats }

create_orders(num_customers=250)



