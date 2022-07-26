import os
import redis

BOOK_KEY = "ru204:book:3"

BOOK = {
  "author": "Redis University",
  "id": 3,
  "description": "This is a fictional book used to demonstrate RedisJSON!",
  "editions": [
    "english",
    "french"
  ],
  "genres": [
    "education",
    "technology"
  ],
  "inventory": [
    {
      "status": "available",
      "stock_id": "3_1"
    },
    {
      "status": "on_loan",
      "stock_id": "3_2"
    }
  ],
  "metrics": {
    "rating_votes": 12,
    "score": 2.3
  },
  "pages": 1000,
  "title": "Up and Running with RedisJSON",
  "url": "https://university.redis.com/courses/ru204/",
  "year_published": 2022
}

# Create a connection to Redis and connect to the server.
if "REDIS_URL" in os.environ:
    REDIS_URL = os.environ["REDIS_URL"]
else:
    REDIS_URL = "redis://localhost:6379/"

print(f"Connecting to Redis at {REDIS_URL}")
r = redis.from_url(REDIS_URL)

# Delete any previous data at our book's key
r.delete(BOOK_KEY)

# Store the book in Redis at key ru204:book:3...
# Response will be: True
response = r.json().set(BOOK_KEY, "$", BOOK)
print(f"Book stored: {response}")

# Let's get the author and score for this book...
# Response will be:
# { '$.author': 'Redis University', '$.metrics.score': 2.3 }
response = r.json().get(BOOK_KEY, "$.author", "$.metrics.score")

print("Author and score:")
print(response)

# Add one to the number of rating_votes:
# Response will be: 13
response = r.json().numincrby(BOOK_KEY, "$.metrics.rating_votes", 1)
print(f"rating_votes incremented to {response}")

# Add another copy of the book to the inventory.
# Response will be: 3 (new size of the inventory array)
response = r.json().arrappend(BOOK_KEY, "$.inventory", {
  "status": "available",
  "stock_id": "3_3"
})
print(f"There are now {response} copies of the book in the inventory.")
