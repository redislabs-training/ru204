# Use Case: Partitioned Stream Example with Python
# Usage: Part of Redis University RU202 courseware
from redis import Redis
import random
from datetime import datetime 
import time
import json
import os

STREAM_BASE = "temps"
STREAM_EXPIRY_TIME = 60 * 10
TEMPERATURE_READING_INTERVAL = 2

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
    
def main():
    redis = Redis(host=os.environ.get("REDIS_HOST", "localhost"),
                  port=os.environ.get("REDIS_PORT", 6379),
                  db=0, decode_responses=True)

    measurement = Measurement()
    previous_stream_key = ""

    while True:
        # Calculate the key for the current stream partition.
        stream_key = STREAM_BASE + ":" + datetime.utcnow().strftime("%Y%m%d%H%M")

        entry = measurement.get_next()
        id = redis.xadd(stream_key, entry, "*")
        print("Wrote " + json.dumps(entry) + " to " + stream_key + " (" + id + ")")

        if (stream_key != previous_stream_key):
            # A new stream partition started, set expiry time for it.
            redis.expire(stream_key, STREAM_EXPIRY_TIME)
            print("Set expiry time for " + stream_key + " (" + str(STREAM_EXPIRY_TIME) + " seconds)")
            previous_stream_key = stream_key

        time.sleep(TEMPERATURE_READING_INTERVAL)

if __name__ == "__main__":
    main()
