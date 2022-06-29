# Redis University RU204: Storing, Querying and Indexing JSON at Speed.
# Python program to read csv file reformat data, and write json objects to 
# individual files named after the base_id.

import json
import io
from random import seed
from random import randint

seed(2)

# Open JSON file.
f = io.open("../data/science_fiction.json", encoding="utf-8")

data = json.load(f)

# Iterating through the JSON.
print(len(data))
for i in data:
    i["base_id"] = i["review_number"]
    i["pages"] = randint(200, 1400)
    i["metrics"] = {
        "score": i["rating_score"],
        "rating_votes": i["rating_votes"]
    }
    del i["review_number"]
    del i["rating_score"]
    del i["rating_votes"]
    del i["original_book_title"]
    i["title"] = i["book_title"]
    del i["book_title"]
    i["author"] = i["author_name"]
    del i["author_name"]
    i["description"] = i["book_description"]
    del i["book_description"]

    num_copies = randint(1, 9)
    print(num_copies)
    status_options = ["on_loan", "available", "maintenance"]
    i["inventory"] = []
    for x in range(num_copies):
        pepper = randint(0,2)
        i["inventory"].append(
            {
                "stock_id": f"{str(i['base_id'])}_{str(x+1)}",
                "status": status_options[(x+pepper)%3]
            }
        )
    
    with open(f"../books/{str(i['base_id'])}.json", "w") as outfile:
        json.dump(i, outfile, indent=4, sort_keys=True)

# Close file.
f.close()
