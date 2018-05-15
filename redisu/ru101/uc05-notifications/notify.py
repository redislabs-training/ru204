"""Use Case: Nofications.
Usage:
Part of Redis University RU101 coursewear"""
from redis import StrictRedis
import os
import time
from datetime import date, timedelta
import random
import threading
import redisu.utils.keynamehelper as keynamehelper
import redisu.ru101.common.generate as generate

redis = None

keynamehelper.set_prefix("uc05")

def create_event(event_sku):
  """Create the event key from the provided details."""
  e_key = keynamehelper.create_key_name("event", event_sku)
  redis.hmset(e_key, {'sku': event_sku})

def purchase(event_sku):
  """Simple purchase function, that pushes the sales order for publishing"""
  qty = random.randrange(1, 10)
  price = 20
  order_id = generate.order_id()
  s_order = {'who': "Jim", 'qty': qty, 'cost': qty * price,
             'order_id': order_id, 'event': event_sku,
             'ts': long(time.time())}
  post_purchases(order_id, s_order)

# def post_purchases(order_id, s_order):
#   """Publishes the Sales Order for listeners to pick up."""
#   so_key = keynamehelper.create_key_name("sales_order", order_id)
#   redis.hmset(so_key, s_order)
#   notify_key = keynamehelper.create_key_name("sales_order_notify")
#   redis.publish(notify_key, order_id)

def post_purchases(order_id, s_order):
  """Publish purchases to the queue."""
  so_key = keynamehelper.create_key_name("sales_order", order_id)
  redis.hmset(so_key, s_order)
  notify_key = keynamehelper.create_key_name("sales_order_notify")
  redis.publish(notify_key, order_id)
  notify_key = keynamehelper.create_key_name("sales_order_notify",
                                             s_order['event'])
  redis.publish(notify_key, order_id)

def listener_sales_analytics(queue):
  """Listener to summarize the sales statistics. Histograms, using
 BITFIELDs are maintained to show sales by hour."""
  l = redis.pubsub(ignore_subscribe_messages=True)
  l.subscribe(queue)
  p = redis.pipeline()
  for message in l.listen():
    order_id = message['data']
    so_key = keynamehelper.create_key_name("sales_order", order_id)
    (ts, qty, event_sku) = redis.hmget(so_key, 'ts', 'qty', 'event')
    hour_of_day = int(time.strftime("%H", time.gmtime(long(ts))))
    vals = ["INCRBY", "u8", (hour_of_day+1) * 8, qty]
    tod_hist_key = keynamehelper.create_key_name("sales_histogram",
                                                 "time_of_day")
    p.execute_command("BITFIELD", tod_hist_key, *vals)
    tod_event_hist_key = keynamehelper.create_key_name("sales_histogram",
                                                       "time_of_day",
                                                       event_sku)
    p.execute_command("BITFIELD", tod_event_hist_key, *vals)
    p.execute()

def listener_events_analytics(queue):
  """Listener to sumamrize total sales by ticket numbers and order value."""
  l = redis.pubsub(ignore_subscribe_messages=True)
  l.subscribe(queue)
  p = redis.pipeline()
  for message in l.listen():
    order_id = message['data']
    so_key = keynamehelper.create_key_name("sales_order", order_id)
    (cost, qty, event_sku) = redis.hmget(so_key, 'cost', 'qty', 'event')
    so_set_key = keynamehelper.create_key_name("sales", event_sku)
    p.sadd(so_set_key, order_id)
    sum_key = keynamehelper.create_key_name("sales_summary")
    p.hincrbyfloat(sum_key, event_sku + ":total_sales", cost)
    p.hincrby(sum_key, event_sku + ":total_tickets_sold", qty)
    p.execute()

def listener_customer_purchases(queue):
  """Listener which post the Invoice details an adds to the customers
 list of Invoices."""
  l = redis.pubsub(ignore_subscribe_messages=True)
  l.subscribe(queue)
  p = redis.pipeline()
  for message in l.listen():
    order_id = message['data']
    so_key = keynamehelper.create_key_name("sales_order", order_id)
    (who, ts, cost) = redis.hmget(so_key, 'who', 'ts', 'cost')
    ts = long(ts)
    inv = {'customer': who,
           'order_date': ts,
           'due_date': date.fromtimestamp(int(ts)) + timedelta(days=90),
           'amount_due': cost,
           'status': "Invoiced"}
    inv_key = keynamehelper.create_key_name("invoice", order_id)
    p.hmset(inv_key, inv)
    cust_set_key = keynamehelper.create_key_name("invoices", who)
    p.sadd(cust_set_key, order_id)
    p.execute()

def print_statistics(stop_event):
  """Thread that prints current event statsistics."""
  sum_key = keynamehelper.create_key_name("sales_summary")
  print "\n === START"
  while not stop_event.is_set():
    print "\n======== {}".format(time.strftime("%a, %d %b %Y %H:%M:%S"))
    e_key = keynamehelper.create_key_name("event", "*")
    for event in redis.scan_iter(match=e_key):
      (_, event_sku) = event.rsplit(":", 1)
      (t_sales, t_tickets) = redis.hmget(sum_key,
                                         event_sku + ":total_sales",
                                         event_sku + ":total_tickets_sold")
      print "Event: {}, Totals Sales: {}, Total Tickets Sold: {}"\
        .format(event_sku, t_sales, t_tickets)
      tod_hist_key = keynamehelper.create_key_name("sales_histogram",
                                                   "time_of_day",
                                                   event_sku)
      hist = redis.get(tod_hist_key)
      if hist != None:
        hist_vals = [hist[i:i+1] for i in range(0, len(hist), 1)]
        print " Histogram: ",
        for i in range(0, 24):
          print " {}/{}".format(i,
                                ord(hist_vals[i]) if i < len(hist_vals) else 0),

      # for i in range(0, 24):
      #   vals = ["GET", "u8", (i+1) * 8]
      #   total_sales = int(redis.execute_command("BITFIELD",
      #                                           tod_hist_key,
      #                                           *vals)[0])
      #   print " {}/{}".format(i, total_sales),
      print "\n"
    time.sleep(1)
  print "\n === END"

# Part One - simple publish & subscribe
def test_pub_sub():
  """Test function for pub/sub messages for fan out"""
  print "== Test 1: Simple pub/sub"
  threads = []
  stop_event = threading.Event()
  queue = keynamehelper.create_key_name("sales_order_notify")
  threads.append(threading.Thread(target=listener_sales_analytics,
                                  args=(queue,)))
  threads.append(threading.Thread(target=listener_events_analytics,
                                  args=(queue,)))
  threads.append(threading.Thread(target=listener_customer_purchases,
                                  args=(queue,)))
  threads.append(threading.Thread(target=print_statistics,
                                  args=(stop_event,)))

  for i in range(len(threads)):
    threads[i].setDaemon(True)
    threads[i].start()

  events = ["Womens Judo", "Mens 4x400"]
  for e in events:
    create_event(e)

  for i in range(15):
    purchase(events[random.randrange(0, len(events))])
    time.sleep(2)
  stop_event.set()
  time.sleep(2)

# Part Two - pattern subscriptions
# def post_purchases(order_id, s_order):
#   """Publish purchases to the queue."""
#   so_key = keynamehelper.create_key_name("sales_order", order_id)
#   redis.hmset(so_key, s_order)
#   notify_key = keynamehelper.create_key_name("sales_order_notify")
#   redis.publish(notify_key, order_id)
#   notify_key = keynamehelper.create_key_name("sales_order_notify",
#                                              s_order['event'])
#   redis.publish(notify_key, order_id)

# Subscribe for 'Opening Ceremony' events, pick every 5th purchase as the
# lottry winner
def listener_oc_alerter(queue):
  """Listener that looks for 'Opening Ceremony' events only. If then tracks
 a Lottery content, award a prize for every 5th order for this event only."""
  l = redis.pubsub(ignore_subscribe_messages=True)
  l.subscribe(queue + ":Opening Ceremony")
  for message in l.listen():
    order_id = message['data']
    sum_key = keynamehelper.create_key_name("sales_summary")
    total_orders = redis.hincrby(sum_key, "Opening Ceremony:total_orders", 1)
    if total_orders % 5 == 0:
      print "===> Winner!!!!! Opening Ceremony Lottery - Order Id: {}"\
        .format(order_id)

# Subscribe to all event, except 'Opening Ceremony' events
def listener_event_alerter(queue):
  """Listener for purchases for events other than 'Opening Ceremony'."""
  l = redis.pubsub(ignore_subscribe_messages=True)
  l.psubscribe(queue + ":[^(Opening)]*")
  for message in l.listen():
    order_id = message['data']
    so_key = keynamehelper.create_key_name("sales_order", order_id)
    (event_sku, qty, cost) = redis.hmget(so_key, 'event', 'qty', 'cost')
    print "Purchase {}: #{} ${}".format(event_sku, qty, cost)

def test_patterned_subs():
  """Test function for patterned subscriptions"""
  print "==Test 2: Patterned subscribers - Opening Ceremony Lottery picker"

  threads_2 = []
  queue = keynamehelper.create_key_name("sales_order_notify")
  threads_2.append(threading.Thread(target=listener_oc_alerter,
                                    args=(queue,)))
  threads_2.append(threading.Thread(target=listener_event_alerter,
                                    args=(queue,)))

  for i in range(len(threads_2)):
    threads_2[i].setDaemon(True)
    threads_2[i].start()

  events = ["Womens Judo", "Mens 4x400", "Opening Ceremony", "Closing Ceremony"]
  for e in events:
    create_event(e)

  for i in range(50):
    purchase(events[random.randrange(0, len(events))])
    time.sleep(random.random())


def main():
  """ Main, used to call test cases for this use case"""
  global redis
  redis = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"),
                      port=os.environ.get("REDIS_PORT", 6379),
                      db=0)
  # Performs the tests
  test_pub_sub()
  test_patterned_subs()

if __name__ == "__main__":
    main()

