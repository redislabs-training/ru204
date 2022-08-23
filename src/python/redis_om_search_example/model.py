from redis_om import (Field, JsonModel, EmbeddedJsonModel)
from pydantic import (PositiveInt, PositiveFloat, AnyHttpUrl)
from typing import List

# This class models the embedded "metrics" object.
class Metrics(EmbeddedJsonModel):
    rating_votes: PositiveInt = Field(index=True)
    score: PositiveFloat = Field(index=True)

# This class models the "inventory" array of objects.
class InventoryItem(EmbeddedJsonModel):
    status: str = Field(index=True)
    stock_id: str = Field(index=True)

# This class models a book.
class Book(JsonModel):
    author: str = Field(index=True)
    id: str = Field(index=True)
    description: str = Field(index=True, full_text_search=True)
    genres: List[str] = Field(index=True)
    inventory: List[InventoryItem]
    metrics: Metrics
    pages: PositiveInt = Field(index=True)
    title: str = Field(index=True, full_text_search=True)
    url: AnyHttpUrl = Field(index=True)
    year_published: PositiveInt = Field(index=True)

    # Extra configuration to specify how to generate key
    # names when saving an instance of the model in Redis.
    class Meta:
        global_key_prefix="ru204:redis-om-python"
        model_key_prefix="book"