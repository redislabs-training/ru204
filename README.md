# RU204: Storing, Querying and Indexing JSON at Speed

## Introduction

This repository contains example data and setup instructions for the Redis University course [RU204: Storing, Querying, and Indexing JSON at Speed](https://university.redis.com/courses/ru204/).

To take this course, you'll first need to do the following:

1. Clone this git repository.
1. Get a Redis instance with RediSearch and RedisJSON installed (we recommend using [Redis Stack](https://redis.io/docs/stack/)).
1. (Optional): Install [RedisInsight](https://redis.com/redis-enterprise/redis-insight/) desktop application (if you choose not to do this you'll use the web version of RedisInsight provided with Redis Stack).  Both are equally good options for this course.
1. Load the course sample data.
1. Build the RediSearch indexes.

To get an appropriate Redis Instance, you can either use the Docker Compose file provided or install [Redis Stack](https://redis.io/docs/stack/) on your machine.

## Clone the Course Git Repository

There are two ways to get a copy of this git repository on your machine...

### Option 1: Use git clone

If you have the [git command line tools](https://git-scm.com/downloads) installed, open up a terminal instance and clone the repository like this:

```bash
git clone https://github.com/redislabs-training/ru204.git
```

Now, change to the directory containing the course files:

```bash
cd ru204
```

The remainder of these instructions assume that you start from a terminal session whose current directory is `ru204`.

### Option 2: Download a Zip File from GitHub

If you don't have the git command line tools, download the repository as a zip file from GitHub and unzip it on your local machine.

![Downloading a zip from GitHub](readme_images/download_zip.png)

Now, open up a terminal instance and change to the directory containing the course files:

```bash
cd ru204
```

The remainder of these instructions assume that you start from a terminal session whose current directory is `ru204`.

## Redis Setup Option 1: Use Docker

First, make sure you have [Docker installed](https://docs.docker.com/get-docker/).

This course uses the Redis Stack Docker container.  Download and start it with Docker Compose as follows:

```bash
docker-compose up -d
```

Check that the container is running like this:

```bash
docker ps
```

You should see output that includes the following:

```
CONTAINER ID IMAGE                    COMMAND          CREATED           STATUS       PORTS                                          NAMES
f7b89c3ca0dd redis/redis-stack:latest "/entrypoint.sh" About an hour ago Up 8 seconds 0.0.0.0:6379->6379/tcp, 0.0.0.0:8001->8001/tcp redisu-ru204
```

## Redis Setup Option 2: Install Redis Stack 

TODO

## RedisInsight Setup

TODO

## You're Ready!

You're now ready to take the course!  If you haven't already, [sign up here](https://university.redis.com/courses/ru204/) to access the course materials.

If you need help or want to chat about all things Redis, [join us on our Discord server](https://discord.gg/46upnugY5B) where you'll find a dedicated channel for this course.