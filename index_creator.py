import argparse
import io
import json
import os
import redis

REDIS_KEY_BASE = "ru204"
INDEX_NAME = "idx:books"

arg_parser = argparse.ArgumentParser(description = "Create RediSearch indexes for RU204.")
arg_parser.add_argument("--redis", default="redis://localhost:6379", dest="redis_url", help="Redis URL to connect to.")
args = arg_parser.parse_args()

print(f"Connecting to Redis at {args.redis_url}")
r = redis.from_url(args.redis_url)

print("Creating search indexes.")

## Work in progress index command:
## ft.create idx:books on json prefix 1 ru204:book: schema $.author as author text sortable $.id as id tag $.description as description text $.editions[*] as editions tag $.genres[*] as genres $.pages as pages numeric sortable $.title as title text sortable $.year_published as year_published numeric sortable $.metrics.rating_votes as rating_votes numeric sortable $.metrics.score as score numeric sortable $.inventory[*].status as status tag $.inventory[*].stock_id as stock_id tag
## TODO how to index genres -- refactor!
# Careful not to drop the docs if doing this after a data load!
#r.ft().dropindex(INDEX_NAME)
#r.ft().create_index()

print("Indexes created.")
r.quit()