# Redis University RU204: Storing, Querying and Indexing JSON at Speed.
# Data loader script.

import argparse
import io
import json
import os
import redis
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.field import TextField, TagField, NumericField

DATASET_SIZE = 1487 # Number of books we expect to load.
REDIS_KEY_BASE = "ru204:book"
INDEX_NAME = "idx:books"

def make_key(book_id):
    return f"${REDIS_KEY_BASE}:{book_id}"

arg_parser = argparse.ArgumentParser(description = "Load JSON data into Redis for RU204.")
arg_parser.add_argument("--dir", dest="books_dir", required=True, help="Directory containing JSON files to load.")
arg_parser.add_argument("--redis", default="redis://localhost:6379", dest="redis_url", help="Redis URL to connect to.")
args = arg_parser.parse_args()

print(f"Connecting to Redis at {args.redis_url}")
r = redis.from_url(args.redis_url)

print("Deleting any existing JSON documents for RU204.")
for k in r.scan_iter(match=make_key("*")):
    r.delete(k)

print("Dropping any existing search index.")
try:
    r.ft(INDEX_NAME).dropindex(delete_documents=False)
except:
    # Dropping an index that doesn't exist throws an exception so
    # let's assume that happened and that this is OK!
    pass

print("Creating search index.")
r.ft(INDEX_NAME).create_index(
    [
        TextField("$.author", as_name="author", sortable=True),
        TagField("$.id", as_name="id"),
        TextField("$.description", as_name="description"),
        TagField("$.editions[*]", as_name="editions"),
        TagField("$.genres[*]", as_name="genres"),
        NumericField("$.pages", as_name="pages", sortable=True),
        TextField("$.title", as_name="title", sortable=True),
        NumericField("$.year_published", as_name="year_published"),
        NumericField("$.metrics.rating_votes", as_name="rating_votes", sortable=True),
        NumericField("$.metrics.score", as_name="score", sortable=True),
        TagField("$.inventory[*].status", as_name="status"),
        TagField("$.inventory[*].stock_id", as_name="stock_id")
    ], 
    definition=IndexDefinition(
        index_type=IndexType.JSON, 
        prefix=[f"${REDIS_KEY_BASE}:"]
    )
)

books_loaded = 0
print(f"Loading JSON files from {args.books_dir}.")
for filename in os.listdir(args.books_dir):
    f = os.path.join(args.books_dir, filename)

    if os.path.isfile(f):
        book_file = io.open(f, encoding="utf-8")
        book = json.load(book_file)
        book_file.close()
        redis_key = make_key(book["id"])
        r.json().set(redis_key, "$", book)
        print(f"Stored book {book['title']} at key {redis_key}.")
        books_loaded += 1

print(f"Loaded {books_loaded} books into Redis.")

# Do some data verification tests...

try:
    # books_loaded should be as expected.
    assert books_loaded == DATASET_SIZE, "Error loading the correct number of books."

    # Book 26 title should be "Banshee in the Well".
    title = r.json().get(make_key("26"), "$.title")
    assert title[0] == "Banshee in the Well", "Error verifying book 26 title."

    # Book 1484 author should be "Terry Pratchett".
    author = r.json().get(make_key("1484"), "$.author")
    assert author[0] == "Terry Pratchett", "Error verifying book 1484 author."

    # Book 253 should have 615 pages.
    num_pages = r.json().get(make_key("253"), "$.pages")
    assert num_pages[0] == 615, "Error verifying book 253 page count."

    # TODO run some sample queries to make sure the data indexing works.
except AssertionError as e:
    print("Data verification checks failed:")
    print(e)
    os._exit(1)

print("Data verification checks completed OK.")

r.quit()
