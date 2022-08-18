# RU204 Redis OM Node Search Example

The following example demonstrates how to search JSON documents stored in Redis using the [Redis OM Node.js](https://github.com/redis/redis-om-node) client.

## Prerequisites

* You'll need [Node.js](https://nodejs.org/) 14.8 or higher installed.
* You will need an instance of Redis Stack.  See the [setup instructions](/README.md) in the README at the root of this repo.
* If you are running your Redis Stack instance in the cloud or somewhere that isn't localhost:6379, you'll need to set the `REDIS_OM_URL` environment variable to point at your instance before running the code.  If you need help with the format for this, check out the [Redis URI scheme specification](https://www.iana.org/assignments/uri-schemes/prov/redis).

## Setup

Install Redis OM and any other dependencies before running the code:

```bash
npm install
```

Ensure that your Redis Stack instance is running, and that you have set the `REDIS_OM_URL` environment variable if necessary.  Example:

```bash
export REDIS_OM_URL=redis://user:password@host:port
```

## Delete Everything in Redis

Delete any data currently in Redis, using the following command in `redis-cli` or the CLI in RedisInsight:

```
FLUSHDB
```

## Load the Sample Data

```bash
npm run load
```

## Run the Sample Queries

```bash
npm run search
```

## View the Code

The code is contained in [`search_om_example.js`](./search_om_example.js).