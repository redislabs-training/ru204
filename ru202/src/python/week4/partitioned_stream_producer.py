# Use Case: Partitioned Stream Example with Python
# Usage: Part of Redis University RU202 courseware
import json
import os
import random
import time
import util.constants as const

from datetime import datetime 
from util.connection import get_connection

# We'll make partitions expire 10 mins apart from
# each other for demo purposes, for a real application
# they might expire after a few days.
#PARTITION_EXPIRY_TIME = 60 * 10 # 10 minutes
PARTITION_EXPIRY_TIME = 60 * 60 * 4 # 4 hours

# Record temperature readings every second.
TEMPERATURE_READING_INTERVAL = 1

# Date that we'll start recording temperatures for - 
# using a future date so that all students get the
# same dataset rather than using dates relative to 
# when the producer is run.  So this timestamp 
# represents the oldest temperature reading that 
# will be generated.
TIMESTAMP_START = 1735689600 # 01/01/2025 00:00:00 UTC

# Number of days of data to generate.
DAYS_TO_GENERATE = 10

ONE_DAY_SECONDS = 60 * 60 * 24

# Utility class to peoduce wandering temperature range.
class Measurement:
    def __init__(self):
        self.current_temp = 50
        self.max_temp = 100
        self.min_temp = 0

    def get_next(self):
        if random.random() >= 0.5:
            if self.current_temp + 1 <= self.max_temp:
                self.current_temp += 1
        elif self.current_temp - 1 >= self.min_temp:
            self.current_temp -= 1

        return {'temp_f': self.current_temp}

# To make this demonstration repeatable, running 
# the producer resets all the streams. 
def reset_state():
    redis = get_connection()

    # Delete any old streams that have not yet expired.
    keys_to_delete = []
    stream_timestamp = TIMESTAMP_START

    for day in range(DAYS_TO_GENERATE):
        keys_to_delete.append(f"{const.STREAM_KEY_BASE}:{datetime.utcfromtimestamp(stream_timestamp).strftime('%Y%m%d')}")
        stream_timestamp += ONE_DAY_SECONDS
        
    # Delete the keys used by the consumers to hold state.
    keys_to_delete.append(const.AGGREGATING_CONSUMER_STATE_KEY)
    keys_to_delete.append(const.AVERAGES_CONSUMER_STATE_KEY)
    keys_to_delete.append(const.AVERAGES_STREAM_KEY)
    
    keys_deleted = redis.delete(*keys_to_delete)
    print("Deleted old streams.")

# Entry point: clean up any old state and run the
# producer.
def main():
    reset_state()

    measurement = Measurement()
    previous_stream_key = ""
    current_timestamp = TIMESTAMP_START

    # End data production a configurable number of days after we began.
    end_timestamp = TIMESTAMP_START + (ONE_DAY_SECONDS * DAYS_TO_GENERATE)

    # Track the stream key names that were generated
    stream_key_names = []

    redis = get_connection()
    
    while current_timestamp < end_timestamp:
        # Calculate the key for the current stream partition.
        # Using one partition per calendar day.  All dates and 
        # times are in UTC.
        stream_key = f"{const.STREAM_KEY_BASE}:{datetime.utcfromtimestamp(current_timestamp).strftime('%Y%m%d')}"
        
        # Get a temperature reading.
        entry = measurement.get_next()
        
        # Publish to the stream.
        redis.xadd(stream_key, entry, current_timestamp)

        # Does this still belong in the stream we're currently 
        # writing to?
        if (stream_key != previous_stream_key):
            # A new day's stream started.
            stream_key_names.append(stream_key)
            
            print(f"Populating stream partition {stream_key}.")
            previous_stream_key = stream_key            

        # Move on to the next timestamp value.
        current_timestamp += TEMPERATURE_READING_INTERVAL

    # Set staggered expiry times on the streams we created.
    # These are set after the streams are all created, as we 
    # are using exact times for this.  For example when 
    # creating 5 stream partitions, the oldest date data 
    # will expire in 10 minutes from when the producer finishes
    # executing, the 2nd in 20, the 3rd in 30, the 4th in 40 and 
    # the most recent data for "today" in 50.  In a real world 
    # application we would set expiry as we finish writing a day's
    # stream.
    days = 1
    current_timestamp = int(time.time())

    # Set the first partition to expire in PARTITION_EXPIRY_TIME seconds.
    # Set subsequent partitions to expire PARTITION_EXPIRY_TIME seconds later
    # than the prior partition.
    for stream_key_name in stream_key_names:
        partition_expires_at = current_timestamp + (days * PARTITION_EXPIRY_TIME)
        print(f"{stream_key_name} expires at {partition_expires_at}")

        # Set expiry time in Redis.
        redis.expireat(stream_key_name, partition_expires_at)

        days += 1

if __name__ == "__main__":
    main()
