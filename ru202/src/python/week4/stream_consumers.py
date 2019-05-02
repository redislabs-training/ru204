# Use Case: Partitioned Stream Example with Python
# Usage: Part of Redis University RU202 courseware
from util.connection import get_connection
import random
from datetime import datetime, timedelta
import time
import json
import os
import sys

STREAM_KEY_BASE = "temps"
LAST_POSITION_KEY = f"consumer_position"

redis = get_connection()

def main():
    current_stream_key = ""
    last_message_id = ""

    # Read stream name and last ID seen from arguments
    # if not supplied, look in Redis for them.
    if len(sys.argv) == 3:
        current_stream_key = sys.argv[1]
        last_message_id = sys.argv[2]
    else:
        h = redis.hgetall(LAST_POSITION_KEY)
        
        if not h:
            print("No stream key and last message ID found in Redis.")
            print("Start the consumer with stream key and last message ID parameters.")
            sys.exit(1)
        else:
            current_stream_key = h["current_stream_key"]
            last_message_id = h["last_message_id"]

    print(f"current_stream_key: {current_stream_key}")
    print(f"last_message_id: {last_message_id}")

    while True:
        # Get the next message from the stream, if any
        streamDict = {}
        streamDict[current_stream_key] = last_message_id
        response = redis.xread(streamDict, count=1, block = 5000)

        if not response:
            # We either need to switch to another stream partition 
            # or wait for more messages to appear on the one we are 
            # on if no newer partitions exist.

            # Work out the name of the stream partition that is one
            # day newer than the current one.
            current_stream_date_str = current_stream_key[-8:]
            current_stream_date = datetime.strptime(current_stream_date_str, "%Y%m%d").date()
            new_stream_date = current_stream_date + timedelta(days = 1)
            new_stream_key = f"{STREAM_KEY_BASE}:{new_stream_date.strftime('%Y%m%d')}"

            # Does the next partition exist?  If so read from it otherwise
            # stick with this stream which will block as we are at the 
            # latest partition now.

            if (redis.exists(new_stream_key) == 1):
                # We are still catching up and have not reached
                # the latest stream partition yet, so move on to
                # consuming the next partition.
                current_stream_key = new_stream_key
                last_message_id = 0                
    
                print(f"Changing to consume stream: {new_stream_key}")
            else:
                # We are currently on the latest stream partition
                # and have caught up with the producer so should 
                # block for a while then try reading it again.      
                print(f"Waiting for new messages in stream: {current_stream_key}")      
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

            # Update the last ID we've seen
            last_message_id = msg_id
            
            # Store current position in Redis.
            redis.hmset(LAST_POSITION_KEY, {
                "current_stream_key": current_stream_key,
                "last_message_id": last_message_id,
            })

if __name__ == "__main__":
    main()
