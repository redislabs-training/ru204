import argparse
import io
import json
import os
import redis

REDIS_KEY_BASE = "ru204"

arg_parser = argparse.ArgumentParser(description = "Create RediSearch indexes for RU204.")
arg_parser.add_argument("--redis", default="redis://localhost:6379", dest="redis_url", help="Redis URL to connect to.")
args = arg_parser.parse_args()

print(f"Connecting to Redis at {args.redis_url}")
r = redis.from_url(args.redis_url)

print("Creating search indexes.")
print("Indexes created.")
r.quit()