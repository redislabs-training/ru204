from model import Book

# Utility function to output matching Book objects.
def print_results(query_description, result_set):
    print(query_description)

    for result in result_set:
        print(f"{result.title} by {result.author} {result.pages} pages, published {result.year_published}.")

    print("-----")

# Search for books written by Stephen King... returns a list
# of Book objects.
result_set = Book.find(
    Book.author == "Stephen King"
).all()

print_results("Stephen King Books", result_set)

# Search for books with 'Star' in the title that are over 500
# pages long, order by length.
result_set = Book.find(
    (Book.title % "Star") & (Book.pages > 500)
).sort_by("pages")

print_results("Star in title, >500 pages", result_set)

# Search for books with 'Star' but not 'War' in the title, and
# which don't have 'space' in the description.
result_set = Book.find(
    (Book.title % "Star") & ~(Book.title % "War") & ~(Book.description % "space")
).all()

print_results("'Star' and not 'War' in title, no 'space' in description", result_set)

# Search for books by Robert Heinlein published between 1959 and 1973,
# sort by year of publication descending.
result_set = Book.find(
    (Book.author == "Robert A. Heinlein") & (Book.year_published > 1958) & (Book.year_published < 1974)
).sort_by("-year_published")

print_results("Robert Heinlein books published x to y", result_set)
