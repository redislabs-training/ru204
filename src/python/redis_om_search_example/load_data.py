import io
import json
import os

from model import Book
from redis_om import Migrator

# Load the sample data set into Book instances and save to Redis
for filename in os.listdir("../../../data/books"):
    f = os.path.join("../../../data/books", filename)

    if os.path.isfile(f):
        book_file = io.open(f, encoding="utf-8")
        book_json = json.load(book_file)
        book_file.close()

        book = Book(**book_json)
        book.save()
        print(f"Stored book {book.title}.")
 
# Create the search index.
Migrator().run()
print("Created search index.")
