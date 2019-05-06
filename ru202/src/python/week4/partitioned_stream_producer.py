# Use Case: Partitioned Stream Example with Python
# Usage: Part of Redis University RU202 courseware
#
# Simulates a temperature logging device that 
# continuously outputs new temperature readings, and
# pushes them into a date-partitioned set of streams 
# in Redis.  A new stream is created for each new 
# day, and set to expire a few days after creation
# to ensure that memory usage is managed.
#
# The producer starts at a configurable date and 
# generates readings for a configurable number of days 
# at a configurable interval.  By default it starts
# on January 1st 2025, generating 10 days worth of 
# data at 1 second intervals.

import json
import os
import random
import time
import util.constants as const

from datetime import datetime 
from util.connection import get_connection

ONE_DAY_SECONDS = 60 * 60 * 24

# Expire stream partitions 2 days after we finish 
# writing to them.
PARTITION_EXPIRY_TIME = ONE_DAY_SECONDS * 2

# Record temperature readings every second.
TEMPERATURE_READING_INTERVAL_SECONDS = 1

# Date that we'll start recording temperatures for - 
# using a future date so that all students get the
# same dataset rather than using dates relative to 
# when the producer is run.  So this timestamp 
# represents the oldest temperature reading that 
# will be generated.
TIMESTAMP_START = 1735689600 # 01/01/2025 00:00:00 UTC

# Number of days of data to generate.
DAYS_TO_GENERATE = 10

# Utility class to produce wandering temperature range.
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

    print("Deleting old streams:")
    for day in range(DAYS_TO_GENERATE):
        stream_key_name = f"{const.STREAM_KEY_BASE}:{datetime.utcfromtimestamp(stream_timestamp).strftime('%Y%m%d')}"
        print(stream_key_name)
        keys_to_delete.append(stream_key_name)
        stream_timestamp += ONE_DAY_SECONDS
        
    keys_deleted = redis.delete(*keys_to_delete)

# Set the expiry time for a stream partition.
def set_expiry(stream_key, expire_at_timestamp):
    redis = get_connection()
    redis.expireat(stream_key, expire_at_timestamp)
    print(f"{stream_key} expires at {datetime.utcfromtimestamp(expire_at_timestamp).strftime('%m/%d/%Y %H:%M:%S')}")

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

    stream_key = ""
    
    while current_timestamp < end_timestamp:
        # Calculate the key for the current stream partition.
        # Using one partition per calendar day.  All dates and 
        # times are in UTC.
        stream_key = f"{const.STREAM_KEY_BASE}:{datetime.utcfromtimestamp(current_timestamp).strftime('%Y%m%d')}"
        
        # Get a temperature reading.
        entry = measurement.get_next()
        
        # Publish to the stream.
        redis.xadd(stream_key, entry, current_timestamp)

        # Have we started a new stream?
        if (stream_key != previous_stream_key):
            # A new day's stream started.
            stream_key_names.append(stream_key)

            # Set expiry time on the partition we just finished writing.
            if previous_stream_key != "":
                set_expiry(previous_stream_key, current_timestamp + PARTITION_EXPIRY_TIME)

            # Now writing to a new partition.
            print(f"Populating stream partition {stream_key}.")
            previous_stream_key = stream_key            

        # Move on to the next timestamp value.
        current_timestamp += TEMPERATURE_READING_INTERVAL_SECONDS
    
    # Set expiry time on the last partition written
    set_expiry(stream_key, current_timestamp + PARTITION_EXPIRY_TIME)

if __name__ == "__main__":
    main()
