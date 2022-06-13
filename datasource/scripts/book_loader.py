# Redis OM defaults to localhost:6379
# This can be overridden by add REDIS_OM_URL env variable with format:
# redis://user:password@hostname:port/db_number'

import os
import io
import json

from redis_om import (
    JsonModel,
    Field,
    Migrator,
)

class Book(JsonModel):
    author_name:str = Field(index=True, full_text_search=True)
    base_id:int = Field(index=True)
    book_description:str = Field(index=True, full_text_search=True)
    book_title:str = Field(index=True, full_text_search=True)
    editions:list[str]
    genres:dict
    inventory:list[dict]
    metrics:dict
    original_book_title:str = Field(index=True, full_text_search=True),
    pages:int = Field(index=True),
    url:str
    year_published:int = Field(index=True)
    
    class Meta:
        global_key_prefix = "book:"

def populate_books(directory):
    # iterate over files in given directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            book_json = io.open(f, encoding="utf-8")
            data = json.load(book_json)
            Book(
                author_name=data['author_name'],
                base_id=data['base_id'],
                book_description=data['book_description'],
                book_title=data['book_title'],
                editions=data['editions'],
                genres=data['genres'],
                inventory=data['inventory'],
                metrics=data['metrics'],
                original_book_title=data['original_book_title'],
                pages=data['pages'],
                url=data['url'],
                year_published=data['year_published']
            ).save()


    Migrator().run()

populate_books('books')
