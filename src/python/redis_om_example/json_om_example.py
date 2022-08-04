from redis_om import (JsonModel, EmbeddedJsonModel)
from pydantic import (PositiveInt, PositiveFloat, AnyHttpUrl)
from typing import List

# This class models the embedded "metrics" object.
class Metrics(EmbeddedJsonModel):
    rating_votes: PositiveInt
    score: PositiveFloat

# This class models the "inventory" array of objects.
class InventoryItem(EmbeddedJsonModel):
    status: str
    stock_id: str

# This class models a book.
class Book(JsonModel):
    author: str
    id: str
    description: str
    genres: List[str]
    inventory: List[InventoryItem]
    metrics: Metrics
    pages: PositiveInt
    title: str
    url: AnyHttpUrl
    year_published: PositiveInt

    # Extra configuration to specify how to generate key
    # names when saving an instance of the model in Redis.
    class Meta:
        global_key_prefix="ru204:redis-om-python"
        model_key_prefix="book"

# Create an instance of the Book model.
new_book = Book(
    author = "Redis Staff",
    id = "999",
    description = "This is a book all about Redis.",
    genres = [ "redis", "tech", "computers" ],
    inventory = [ 
        InventoryItem(
            status = "on_loan",
            stock_id = "999_1"
        ),
        InventoryItem(
            status = "maintenance",
            stock_id = "999_2"
        )
    ],
    metrics = Metrics(
        rating_votes = 4000,
        score = 4.5
    ),
    pages = 1000,
    title = "Redis for Beginners",
    url = "https://university.redis.com/courses/ru204/",
    year_published = 2022
)

# Get the locally generated ULID for this book.
print(f"new_book ULID: {new_book.pk}")

# Save the book to Redis.
new_book.save()
print("Saved book in Redis.")

# Retrieve the book from Redis.
a_book = Book.get(new_book.pk)
print("Retrieved from Redis:")
print(a_book)

# Update the author field and save it.
a_book.author = "Redis University"
a_book.save()
print("Updated author and saved to Redis:")
print(Book.get(new_book.pk))
