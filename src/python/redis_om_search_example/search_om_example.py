from redis_om import (JsonModel, EmbeddedJsonModel, Migrator)
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
        global_key_prefix="ru204"
        model_key_prefix="book"

# Create the search index.
Migrator().run()

# TODO search for things...

