# RU204 Node-Redis Example

The following example demonstrates the execution of RedisJSON commands using the [Node-Redis](https://github.com/redis/node-redis) client.

## Prerequisites

* You'll need [Node.js](https://nodejs.org/) 14.8 or higher installed.
* You wll need an instance of Redis Stack.  See the [setup instructions](/README.md) in the README at the root of this repo.
* If you are running your Redis Stack instance in the cloud or somewhere that isn't localhost:6379, you'll need to set the `REDIS_URL` environment variable to point at your instance before running the code.  If you need help with the format for this, check out the [Redis URI scheme specification](https://www.iana.org/assignments/uri-schemes/prov/redis).

## Setup

Install Node-Redis and any other dependencies before running the code:

```bash
npm install
```

Ensure that your Redis Stack instance is running, and that you have set the `REDIS_URL` environment variable if necessary.  Example:

```bash
export REDIS_URL=redis://user:password@host:port
```

## Run the Code

```bash
npm start
```

## View the Code

The code is contained in [`json_example.js`](./json_example.js).
