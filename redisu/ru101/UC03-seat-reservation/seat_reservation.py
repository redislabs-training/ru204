from redis import StrictRedis, WatchError
import os
import string
import json
import math
import random
import struct
import redisu.utils.keynamehelper as keynamehelper
import redisu.utils.textincr as textincr
import redisu.ru101.common

redis = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"), 
                    port=os.environ.get("REDIS_PORT", 6379),
                    db=0)

keynamehelper.set_prefix("uc03:")

__max__seats_per_block__=32
def create_event(event_sku, blocks=2, seat_per_block=32, tier="General"):
	block_name = "A"
	for i in range(blocks):
		filled_seat_map = int(math.pow(2,min(seat_per_block, __max__seats_per_block__)))-1
		vals = ["SET", "u32", 0, filled_seat_map]
		key = keynamehelper.create_key_name("seatmap", event_sku, tier, block_name)
		redis.execute_command("BITFIELD", key, *vals)
		block_name = textincr.incr_str(block_name)

def get_event_seat_block(event_sku, tier, block_name):
	vals = ["GET", "u32", 0]
	key = keynamehelper.create_key_name("seatmap", event_sku, tier, block_name)
	return	redis.execute_command("BITFIELD", key, *vals)[0]

def print_event_seat_map(event_sku, tier="*"):
	key = keynamehelper.create_key_name("seatmap", event_sku, tier, "*")
	blocks = redis.keys(key)
	for block in blocks:
		(_, tier_name, block_name) = block.rsplit(":", 2)
		seat_map = get_event_seat_block(event_sku, tier_name, block_name)
		print("{:40s} ").format(block),
		for i in range(seat_map.bit_length()):
			if ((i % 10 ) == 0):
				print "|",
			print (seat_map >> i) & 1,
		print "|"

# Part One - Create the event map
event = "123-ABC-723"
create_event(event)
print_event_seat_map(event)

def get_availbale(seat_map, seats_required, first_seat=-1):
	seats = []
	if ( first_seat != -1 ):
		end_seat = first_seat + seats_required -1
	else:
		end_seat = seat_map.bit_length()+1
	required_block = int(math.pow(2,seats_required))-1
	for i in range(1, end_seat+1):
		if ( (seat_map & required_block) == required_block ):
			seats.append( {'first_seat': i, 'last_seat': i + seats_required -1} )
		required_block = required_block << 1
	return seats

def find_seat_selection(event_sku, tier, seats_required):
	# Get all the seat rows
	seats = []
	key = keynamehelper.create_key_name("seatmap", event_sku, tier, "*")
	blocks = redis.keys(key)
	for block in blocks:
		# Find if there are enough seats in the row, before checking if they are contiguous
		if ( redis.bitcount(block) >= seats_required ):
			(_, tier_name, block_name) = block.rsplit(":", 2)
			seat_map = get_event_seat_block(event_sku, tier_name, block_name)
			block_availability = get_availbale(seat_map, seats_required)
			if (len(block_availability) > 0):
				seats.append( {'event': event_sku, 'tier' : tier_name, 'block': block_name, 'available': block_availability } )
		else:
			print "Row '{}' does not have enough seats".format(block)
	return seats

def print_seat_availbailiy(seats):
	for block in seats:
		print "Event: {}".format(block['event'])
		current_block = block['available']
		for i in range(len(current_block)):
			print "-Row: {}, Start {}, End {}".format(block['block'],current_block[i]['first_seat'], current_block[i]['last_seat'],)

def set_seat_map(event_sku, tier, block_name, map):	
	vals = ["SET", "u32", 0, map]
	key = keynamehelper.create_key_name("seatmap", event_sku, tier, block_name)
	redis.execute_command("BITFIELD", key, *vals)

available_seats = find_seat_selection(event, "General", 15)
print_seat_availbailiy(available_seats)

# Check that we skip rows
set_seat_map(event, "General", "A", int(math.pow(2, 20) - 31))
print_event_seat_map(event)
available_seats = find_seat_selection(event, "General", 16)
print_seat_availbailiy(available_seats)

# Part Two - reserve seats
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class SeatTaken(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

def reservation(event_sku, tier, block_name, first_seat, last_seat):
	reserved = False
	p = redis.pipeline()
	try:
		seat_map = get_event_seat_block(event_sku, tier, block_name)
		seats = get_availbale(seat_map, last_seat - first_seat + 1, first_seat)
		if ( len(seats) > 0 ):
			for i in range(first_seat, last_seat+1):
				# Reserve individual seat, raise exception is already reserved
				seat_key = keynamehelper.create_key_name("seatres", event_sku, tier, block_name, str(i))
				if (redis.set(seat_key, True,	px=5000, nx=True) != True):
					raise SeatTaken(i, "event:" + event_sku + ":" + block_name + ":" + str(i))
			order_id = redisu.ru101.common.generate_order_id()
			required_block = int(math.pow(2,last_seat - first_seat + 1))-1 << (first_seat-1)
			vals = ["SET", "u32", 0, required_block]
			order_key = keynamehelper.create_key_name("seatres", event_sku, tier, block_name, order_id)
			p.execute_command("BITFIELD", order_key, *vals)
			p.expire(order_key, 5)
			block_key = keynamehelper.create_key_name("seatmap", event_sku, tier, block_name)
			p.bitop("XOR", block_key, 
				             block_key, 
				             order_key)
			p.execute()
			reserved = True
	except SeatTaken as error:
		print "Seat Taken/{}".format(error.message)
	finally:
		p.reset()
	return reserved

event="737-DEF-911"
seats=10
create_event(event, 1, seats, "VIP")
# Seat 4 (the 8th bit) is already sold. We calc this as (2^(seats)-1) - bit_number_of_seat, e.g. 1023 - 8
set_seat_map(event, "VIP", "A", int(math.pow(2, seats)-1-8))
print_event_seat_map(event)

seats = find_seat_selection(event, "VIP", 2)
print_seat_availbailiy(seats)
# Just choose the first found
made_reservation = reservation(event, "VIP", seats[0]['block'], seats[0]['available'][0]['first_seat'], seats[0]['available'][0]['last_seat'])
print "Made reservation? {}".format(made_reservation)
print_event_seat_map(event)

# Find space for 5 seats
seats = find_seat_selection(event, "VIP", 5)
print_seat_availbailiy(seats)
# Just choose the first found
made_reservation = reservation(event, "VIP", seats[0]['block'], seats[0]['available'][0]['first_seat'], seats[0]['available'][0]['last_seat'])
print "Made reservation? {}".format(made_reservation)
print_event_seat_map(event)

# Find space for 2 seat, but not enough inventory
seats = find_seat_selection(event, "VIP", 2)
if ( len(seats) == 0 ):
	print "Not enough seats"

# Find space for 1 seat
seats = find_seat_selection(event, "VIP", 1)
# Create a seat reservation (simulating another user), so that the reservation fails
key = keynamehelper.create_key_name("seatres", event, "VIP", seats[0]['block'], str(seats[0]['available'][0]['first_seat']))
redis.set(key, True, px=5000)
made_reservation = reservation(event, "VIP", seats[0]['block'], seats[0]['available'][0]['first_seat'], seats[0]['available'][0]['last_seat'])
print "Made reservation? {}".format(made_reservation)
print_event_seat_map(event)


