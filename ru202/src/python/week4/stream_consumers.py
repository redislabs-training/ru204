# Use Case: Partitioned Stream Example with Python
# Usage: Part of Redis University RU202 courseware
from redis import Redis
import random
from datetime import datetime, timedelta
import time
import json
import os
import sys

STREAM_KEY_BASE = "temps"
LAST_POSITION_KEY = f"consumer_position"

redis = Redis(host=os.environ.get("REDIS_HOST", "localhost"),
                port=os.environ.get("REDIS_PORT", 6379),
                db=0, decode_responses=True)
    
def main():
    current_stream_key = ""
    last_message_id = ""

    # Today's stream key, used for knowing when to stop.
    # TODO what if we catch up with today during today?
    today_stream_key = f"{STREAM_KEY_BASE}:20250110"

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
        response = redis.xread(streamDict, count=1)

        if not response:
            # We have exhausted this stream, try for another partition
            print(f"Stream {current_stream_key} exhausted.")

            # If this is today's stream then we are done.
            if current_stream_key == today_stream_key:
                print("Caught up to today...")
                sys.exit()

            # Work out the name of the stream partition that is one
            # day newer than the current one.
            current_stream_date_str = current_stream_key[-8:]
            current_stream_date = datetime.strptime(current_stream_date_str, "%Y%m%d").date()
            new_stream_date = current_stream_date + timedelta(days = 1)
            new_stream_key = STREAM_KEY_BASE + ":" + new_stream_date.strftime("%Y%m%d")
            
            print(f"Last ID was {last_message_id}")
            print(f"Next stream should be {new_stream_key}")

            # Set the stream key and reset the ID
            current_stream_key = new_stream_key
            last_message_id = 0
        else:
            # Read the response that we got from Redis
            msg = response[0][1][0]

            # Get the ID of the message that was just read.
            msg_id = msg[0]
            print(str(msg_id))

            # Get the timestamp value from the message ID 
            # (everything before the - in the ID).
            msg_timestamp = msg_id.split("-")[0]
            print(msg_timestamp)

            # Get the temperature value from the message.
            msg_temperature = msg[1]['temp_f']
            print(msg_temperature)

            # Update the last ID we've seen
            last_message_id = msg_id
            
            # Store current position in Redis.
            redis.hmset(LAST_POSITION_KEY, {
                "current_stream_key": current_stream_key,
                "last_message_id": last_message_id,
            })

if __name__ == "__main__":
    main()
