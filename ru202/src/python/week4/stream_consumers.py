# Use Case: Partitioned Stream Example with Python
# Usage: Part of Redis University RU202 courseware
from multiprocessing import Process
from util.connection import get_connection
import util.constants as const
import random
from datetime import datetime, timedelta
import time
import json
import os
import sys

#STREAM_KEY_BASE = "temps"
#AGGREGATING_CONSUMER_STATE_KEY = "aggregating_consumer_state"
#AVERAGES_CONSUMER_STATE_KEY = "averages_consumer_state"
#AVERAGES_STREAM_KEY = f"{STREAM_KEY_BASE}:averages"

AGGREGATING_CONSUMER_PREFIX = "agg"
AVERAGES_CONSUMER_PREFIX = "avg"

def log(prefix, message):
    if prefix == AVERAGES_CONSUMER_PREFIX:
        print(f"\033[93m{prefix}: {message}\033[0m")
    else:
        print(f"{prefix}: {message}")

def aggregating_consumer_func(current_stream_key, last_message_id):
    log(AGGREGATING_CONSUMER_PREFIX, f"Starting aggregating consumer in stream {current_stream_key} at message {last_message_id}.")

    redis = get_connection()

    while True:
        # Get the next message from the stream, if any
        streamDict = {}
        streamDict[current_stream_key] = last_message_id
        response = redis.xread(streamDict, count = 1, block = 5000)

        if not response:
            # We either need to switch to another stream partition 
            # or wait for more messages to appear on the one we are 
            # on if no newer partitions exist.

            # Work out the name of the stream partition that is one
            # day newer than the current one.
            current_stream_date_str = current_stream_key[-8:]
            current_stream_date = datetime.strptime(current_stream_date_str, "%Y%m%d").date()
            new_stream_date = current_stream_date + timedelta(days = 1)
            new_stream_key = f"{const.STREAM_KEY_BASE}:{new_stream_date.strftime('%Y%m%d')}"

            # Does the next partition exist?  If so read from it otherwise
            # stick with this stream which will block as we are at the 
            # latest partition now.

            if (redis.exists(new_stream_key) == 1):
                # We are still catching up and have not reached
                # the latest stream partition yet, so move on to
                # consuming the next partition.
                current_stream_key = new_stream_key
                last_message_id = 0                
    
                log(AGGREGATING_CONSUMER_PREFIX, f"Changing to consume stream: {new_stream_key}")
            else:
                # We are currently on the latest stream partition
                # and have caught up with the producer so should 
                # block for a while then try reading it again.      
                log(AGGREGATING_CONSUMER_PREFIX, f"Waiting for new messages in stream {current_stream_key}")      
        else:
            # Read the response that we got from Redis
            msg = response[0][1][0]

            # Get the ID of the message that was just read.
            msg_id = msg[0]
            #print(str(msg_id))

            # Get the timestamp value from the message ID 
            # (everything before the - in the ID).
            msg_timestamp = msg_id.split("-")[0]
            #print(msg_timestamp)

            # Get the temperature value from the message.
            msg_temperature = msg[1]['temp_f']
            #print(msg_temperature)

            # TODO do some calculation and put a result on
            # another stream periodicially.
            # Temporary logic to push some things to second stream...
            if (float(msg_temperature) > 65.0):
                payload = {
                    'average_temp_f': msg_temperature,
                    'timestamp': msg_timestamp
                }

                # Publish result, trimming the stream each time a new message
                # is added.
                new_msg_id = redis.xadd(const.AVERAGES_STREAM_KEY, payload, "*", maxlen = 20, approximate = True)
                log(AGGREGATING_CONSUMER_PREFIX, f"Published aggregated result ID {new_msg_id} to {const.AVERAGES_STREAM_KEY}.")

            # Update the last ID we've seen
            last_message_id = msg_id
            
            # Store current state in Redis.
            redis.hmset(const.AGGREGATING_CONSUMER_STATE_KEY, {
                "current_stream_key": current_stream_key,
                "last_message_id": last_message_id
            })

def averages_consumer_func():
    redis = get_connection()

    # Recover our last message ID context or default to 0
    last_message_id = "0"
    h = redis.hgetall(const.AVERAGES_CONSUMER_STATE_KEY)
    
    if h:
        last_message_id = h["last_message_id"]

    log(AVERAGES_CONSUMER_PREFIX, f"Starting averages consumer in stream {const.AVERAGES_STREAM_KEY} at message {last_message_id}.")

    while True:
        # Get the next message from the stream, if any
        streamDict = {}
        streamDict[const.AVERAGES_STREAM_KEY] = last_message_id
        response = redis.xread(streamDict, count = 1, block = 5000)    

        if response:
            msg = response[0][1][0]

            # Get the ID of the message that was just read.
            msg_id = msg[0]   

            # Get the average temperature value from the message.
            msg_average_temperature = msg[1]['average_temp_f']

            # Get the timestamp value from the message.
            msg_timestamp = msg[1]['timestamp']

            log(AVERAGES_CONSUMER_PREFIX, f"Average temperature for {msg_timestamp} was {msg_average_temperature}F.")

            # Update our last message for the next XREAD.
            last_message_id = msg_id

            # Store current state in Redis.
            redis.hmset(const.AVERAGES_CONSUMER_STATE_KEY, {
                "last_message_id": last_message_id
            })
        else:
            log(AVERAGES_CONSUMER_PREFIX, f"Waiting for new messages in stream {const.AVERAGES_STREAM_KEY}")


def main():
    current_stream_key = ""
    last_message_id = ""
    redis = get_connection()

    # Read stream name and last ID seen from arguments
    # if not supplied, look in Redis for them.
    if len(sys.argv) == 3:
        current_stream_key = sys.argv[1]
        last_message_id = sys.argv[2]
    else:
        h = redis.hgetall(const.AGGREGATING_CONSUMER_STATE_KEY)
        
        if not h:
            print("No stream key and last message ID found in Redis.")
            print("Start the consumer with stream key and last message ID parameters.")
            sys.exit(1)
        else:
            current_stream_key = h["current_stream_key"]
            last_message_id = h["last_message_id"]

    # Start the aggregating consumer process.
    aggregating_consumer = Process(target = aggregating_consumer_func, args = (current_stream_key, last_message_id, ))
    aggregating_consumer.start()

    # Start the averages consumer process.
    averages_consumer = Process(target = averages_consumer_func, args = ())
    averages_consumer.start()

if __name__ == "__main__":
    main()
