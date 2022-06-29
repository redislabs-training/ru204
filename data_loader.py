# Redis University RU204: Storing, Querying and Indexing JSON at Speed.
# Data loader script.

import argparse
import io
import json
import os
import redis

REDIS_KEY_BASE = "ru204"

def make_key(book_id):
    return f"{REDIS_KEY_BASE}:books:{book_id}"

arg_parser = argparse.ArgumentParser(description = "Load JSON data into Redis for RU204.")
arg_parser.add_argument("--dir", dest="books_dir", required=True, help="Directory containing JSON files to load.")
arg_parser.add_argument("--redis", default="redis://localhost:6379", dest="redis_url", help="Redis URL to connect to.")
args = arg_parser.parse_args()

print(f"Connecting to Redis at {args.redis_url}")
r = redis.from_url(args.redis_url)

books_loaded = 0
print(f"Loading json files from {args.books_dir}")
for filename in os.listdir(args.books_dir):
    f = os.path.join(args.books_dir, filename)

    if os.path.isfile(f):
        book_file = io.open(f, encoding="utf-8")
        book = json.load(book_file)
        book_file.close()
        redis_key = make_key(book["base_id"])
        r.json().set(redis_key, "$", book)
        print(f"Stored book {book['title']} at key {redis_key}.")
        books_loaded += 1

print(f"Loaded {books_loaded} books into Redis.")

# Do some data verification tests...

try:
    # books_loaded should be 670.
    assert books_loaded == 670, "Error loading the correct number of books."

    # Book 23 title should be "Saving Sara".
    title = r.json().get(make_key("23"), "$.title")
    assert title[0] == "Saving Sara", "Error verifying book 23 title."

    # Book 1484 author should be "Charlie Jane Anders".
    author = r.json().get(make_key("1484"), "$.author")
    assert author[0] == "Charlie Jane Anders", "Error verifying book 1484 author."

    # Book 13517 should have 1000 pages.
    num_pages = r.json().get(make_key("13517"), "$.pages")
    assert num_pages[0] == 1000, "Error verifying book 13517 page count."
except AssertionError as e:
    print("Data verification checks failed:")
    print(e)
    os._exit(1)

print("Data verification checks completed OK.")

r.quit()