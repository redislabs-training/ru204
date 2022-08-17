from model import Book

# Search for books written by Stephen King...
result_set = Book.find(
    Book.author == "Stephen King"
).all()

print(result_set)

# TODO others

