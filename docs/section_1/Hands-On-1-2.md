# Hands-On Exercise: Storing JSON with Redis native data types

Throughout this exercise, we will use this simplified book JSON document as an example. This is an abbreviated form of the book JSON document found within this course's same data set.

```json
{
    "base_id": 18161,
    "title": "Obsidian",
    "pages": 999,
    "inventory": [
        {
            "stock_number": "18161_1",
            "status": "on_loan"
        },
        {
            "stock_number": "18161_3",
            "status": "maintenance"
        }
    ],
    "genres": {
        "Young Adult": 3439, 
        "Fantasy": 2545, 
        "Science Fiction (Aliens) ": 1648, 
        "Science Fiction": 1170
    }
}
```

## Strings
For this first exercise we will store Raw JSON in Redis as a String.

In RedisInsight or `redis-cli`, use the `SET` command to store Raw JSON as a string.

```bash
> SET JSON:serialized-string '{"base_id": 18161,"title": "Obsidian", "pages": 999, "inventory": [{"stock_number": "18161_1","status": "on_loan"},{"stock_number": "18161_3","status": "maintenance"}],"genres": {"Young Adult": 3439, "Fantasy": 2545, "Science Fiction (Aliens) ": 1648, "Science Fiction": 1170} }'
OK
```

> Note that while Raw JSON is stored as a String within Redis, specific data types cannot be directly accessed or manipulated, as the format is a String primitive and is not recognized as an organized document


Retrieve the `JSON:serialized-string` with the `GET` command.

```bash
> GET JSON:serialized-string
"{\"base_id\": 18161,\"title\": \"Obsidian\", \"pages\": 999, \"inventory\": [{\"stock_number\": \"18161_1\",\"status\": \"on_loan\"},{\"stock_number\": \"18161_3\",\"status\": \"maintenance\"}],\"genres\": {\"Young Adult\": 3439, \"Fantasy\": 2545, \"Science Fiction (Aliens) \": 1648, \"Science Fiction\": 1170} }"
```

This may be an adequate storage solution if an application uses predictably small JSON documents that do not need manipulation or sub-document access.

## Hashes
The Redis Hash data type is a valid alternative to Strings if the JSON document is flat. Nested objects and lists cannot be stored within Hashes. This can be solved by serializing these sub-documents as strings and stored as fields within the Hash.

```bash
> HSET JSON:hash base_id 18161 title Obsidian pages 999 inventory '[{"stock_number": 18161_1, "status": "on_loan"},{"stock_number": 18161_3, "status": "maintenance"}]' genres '{"Young Adult": 3439, "Fantasy": 2545, "Science Fiction (Aliens)":  1648, "Science Fiction": 1170}'
(integer) 5
```

When retrieving the JSON document that has been stored as a hash, top-level Number and String data types are easily accessible, but ebedded objects and nested lists are not.

Retrieving a top-level field containing a number:
```bash
> HGET JSON:hash pages
"999"
```

Retrieving a top-level field containing a string:
```bash
> HGET JSON:hash title
"Obsidian"
```

Retrieving a nested list containing objects:
```bash
> HGET JSON:hash inventory
"[{\"stock_number\": 18161_1, \"status\": \"on_loan\"},{\"stock_number\": 18161_3, \"status\": \"maintenance\"}]"
```

Hashes will bring JSON documents one step closer to full document retrieval and manipulation, but many fields will still need to be deserialized.

## JSON documents spanning multiple keys

This is complex if not extreme example of storing individual fields of JSON as separate data types within Redis.  This method requires a strict key naming methodology and an expensive amount of trips to and from the Redis server to retrieve the necessary fields.

Sub-documents (lists and objects) within a JSON document will have their own separate Redis keys, with said keys referenced in the parent JSON object.

First create the top-level JSON object as a hash. We will use the key name `book:18161`

```bash
> HSET book:18161 base_id 18161 title Obsidian pages 999 inventory book:18161:inventory genres book:18161:genres
(integer) 5
```

Notice that the `inventory` field now refers to the value `book:18161:inventory`, which will be the key name storing a list of key names referencing individual hash objects. 'genres' references the key name `book:18161:genres` which will be a separate hash.

Now create the `book:18161:inventory` list:
```bash
> LPUSH book:18161:inventory book:18161:inventory:18161_1 book:18161:inventory:18161_3
(integer) 2
```

Each element within the list will be a hash. Create the two hashes with the key names `book:18161:inventory:18161_1` and `book:18161:inventory:18161_3`` respectively.

```bash
> HSET book:18161:inventory:18161_1 stock_number 18161_1 status on_loan
(integer) 2
```

```bash
> HSET book:18161:inventory:18161_3 stock_number 18161_3 status maintenance
(integer) 2
```

Lastly, create the `book:18161:genres` hash.

```bash
> HSET book:18161:genres "Young Adult" 3439 "Fantasy" 2545 "Science Fiction (Aliens)" 1648 "Science Fiction" 1170
(integer) 4
```

We have now "flattened" the sample book JSON document enough into separate Redis native data types to retrieve and update every individual field and sub-document.  If this particular exercise felt cumbersome and unwieldy, that is expected and intended. A client would need to send multiple requests to the Redis server to retrieve a single value based on the key name referencing and look up. Hopefully this will excite you for the full capabilitys of RedisJSON!

