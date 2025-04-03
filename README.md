# RU204: Redis JSON

## Introduction

This repository contains example data and setup instructions for the [Redis JSON](https://university.redis.io/learningpath/6q3tbh3qk2gexx?tab=details) learning path on [Redis University](https://university.redis.io/).

To take this course, you'll first need to do the following:

1. Make sure that you have Python 3.7 or newer installed on your system (we've tested this with Python 3.9).  Check your Python version with `python --version`.
1. Clone this git repository from GitHub.
1. Get a [Redis Stack](https://redis.io/docs/stack/) instance locally or in the cloud.
1. Install [RedisInsight](https://redis.com/redis-enterprise/redis-insight/).
1. Load the course sample data and create the search index.

We've provided detailed instructions for each of these steps below.

Throughout the course, we've provided example code written in Python, JavaScript (Node.js), Java and C#.  You don't need to run the code to be successful on this course, and the exam does not contain programming language specific questions.  If you'd like to try running some or all of the code samples then you'll also need to install:

* [Node.js](https://nodejs.org/) (version 14.8 or higher)
* [Java JDK](https://sdkman.io/) (Java 11 or higher)
* [.NET SDK](https://dotnet.microsoft.com/en-us/download/dotnet/6.0) (version 6 or higher)

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

Your next step is to proceed to "Redis Setup".

### Option 2: Download a Zip File from GitHub

If you don't have the git command line tools, download the repository as a zip file from GitHub and unzip it on your local machine.

![Downloading a zip from GitHub](readme_images/download_zip.png)

Now, open up a terminal instance and change to the directory containing the course files:

```bash
cd ru204
```

The remainder of these instructions assume that you start from a terminal session whose current directory is `ru204`.  

Your next step is to proceed to "Redis Setup".

## Redis Setup 

This course requires an instance of Redis with the RediSearch and RedisJSON modules installed.  These are part of the Redis Stack product.  Review the following options and choose the one that's right for you.

### Option 1: Redis Cloud

This option doesn't require you to install Redis on your local machine.  We provide a free instance of Redis in the cloud that you can keep and use for your own projects once you're finished with the course.  

Let's get up and running with Redis in the cloud:

* Use your browser to navigate to the [signup page](https://redis.com/try-free?utm_medium=referral&utm_source=redisUniversity&utm_campaign=ru204) on redis.com.
* Complete the signup form and click the "Get Started" button.  Note that you can sign up with your Google or GitHub account if you prefer.
* When you receive the activation email from Redis, open it and click on the "Activate Account" button.
* You'll be taken to the dashboard, and a New Subscription dialog appears:

![Redis Cloud New Subscription](readme_images/cloud_new_sub_1.png)

* Select your preferred cloud provider and a region close to you.  This is where we'll host your free Redis instance for you.
* Click the "Let's start free" button.
* Your new free database will be created, and you should see something like this:

![Redis Cloud newly created database](readme_images/cloud_new_sub_2.png)

* Click on "Redis-free-db" to drill down into the details for your instance.
* To set up RedisInsight and connect the course data loader script to your database, you'll need to gather the following items from the dashboard and keep a record of them:
  * Host name
  * Port
  * User name (this will be `default`)
  * Password
* Your host name and port can be found in the "General" section (see below for example, here the host name is `redis-15676.c10.us-east-1-3.ec2.cloud.redislabs.com` and the port is `15676`).

![Redis Cloud database details](readme_images/cloud_new_sub_3.png)

* Scroll down to the "Security" section.
* Click the "Copy" button next to "Default user password" to copy the Redis password into the clipboard.  Paste this somewhere for safekeeping.  Alternatively, click the eye icon to show the password:

![Redis Cloud database password](readme_images/cloud_new_sub_4.png)

* If you see a green check mark next to the "Redis-free-db" title, your database is ready to use!

Your next step is to set up RedisInsight...

### Option 2: Docker

This is the most straightforward option if you want to run Redis locally.  First, make sure you have [Docker installed](https://docs.docker.com/get-docker/).

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

Leave the container running for now. When you want to stop it, use this command:

```bash
docker-compose down
```

The container will persist Redis data to the `redisdata` folder.

Your next step is to set up RedisInsight...

### Option 3: Install Redis Stack 

Redis Stack can be installed using popular package managers for macOS and Linux.  [Follow the instructions on redis.io](https://redis.io/docs/stack/get-started/install/) to install and start Redis Stack.

Your next step is to set up RedisInsight...

## RedisInsight Setup

RedisInsight is a graphical interface allowing you to interact with data and configure Redis instances.

### Option 1: Install and Configure the Desktop Application

The preferred way to run RedisInsight is as a desktop application.  If you're using a Redis instance in the cloud, you'll need to install the RedisInsight desktop application.  If you chose the Docker or local install of Redis Stack option for your Redis instance, you can either install the RedisInsight desktop application or choose run it as a web application with no further software installation required (see option 2 below).

To use the desktop application, first download and install it using the instructions on the [RedisInsight download page](https://redis.com/redis-enterprise/redis-insight/).  

Once you have installed RedisInsight, start it up and agree to the terms and conditions of use. 

Finally, configure RedisInsight to connect to your Redis Instance... Click the "ADD REDIS DATABASE" button and fill out the new database form with the following values.

If your Redis instance is in the cloud:

* **Host:** The host name for your cloud database
* **Port:** The port number for your cloud database
* **Database Alias:** RU204
* **Username:** default
* **Password:** The password for your cloud database
* **Select Logical Database:** [leave unchecked]
* **Use TLS:** [leave unchecked]

If you are using Docker or you have installed Redis Stack locally:

* **Host:** localhost
* **Port:** 6379
* **Database Alias:** RU204
* **Username:** [leave blank]
* **Password:** [leave blank]
* **Select Logical Database:** [leave unchecked]
* **Use TLS:** [leave unchecked]

Then click the "Add Redis Database" button to connect to your Redis instance.  You should see "RU204" in the list of Redis databases, and can click on it to open the Browser view.

![Configuring RedisInsight Desktop](readme_images/insight_setup.gif)

If you see an error while trying to connect to Redis, ensure that your Redis instance is running (make sure the Docker container is up or your locally installed Redis Stack is running) and try again.

Your next step is to load the sample data...

### Option 2: Use the Web Interface

If you used the Docker or local install of Redis Stack options to get your Redis instance, you can choose to use RedisInsight as a web application with no further software to install.  If you're using a Redis instance in the cloud, this option is not currently available to you and you should download and install RedisInsight instead.

First, ensure that the Docker container or your local Redis Stack installation is running.

Now, point your browser at `http://localhost:8001/` and you should see the RedisInsight terms and conditions:

![RedisInsight web terms and conditions](readme_images/insight_web_terms.png)

Accept the terms and click "Submit".  RedisInsight will automatically connect to the local Redis Stack instance and display the key browser:

![RedisInsight web interface](readme_images/insight_web.png)

Your next step is to load the sample data...

## Load the Sample Data into Redis and Create the Search Index

This course uses a sample data set consisting of almost 1500 JSON documents, each containing details about a science fiction book.  These documents are contained in the `data/books` folder.

Before starting the course, you'll need to use the data loader to load these documents into Redis.  The data loader also sets up a RediSearch index that you'll use to search the document collection.

First, with your shell in the `ru204` folder create a Python virtual environment, activate it and install the dependencies required to run the data loader:

```bash
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

Now run the data loader script, passing it the name of the folder containing the JSON data files to load into Redis.

If your Redis instance is in the cloud, start the data loader like this:

```bash
python data_loader.py --dir data/books --redis redis://default:password@host:port/
```

Be sure to replace `password`, `host` and `port` with the values for your cloud instance.

If you're using Docker, or have installed Redis Stack locally, start the data loader this way:

```bash
python data_loader.py --dir data/books
```

You should expect to see output similar to the following:

```
Connecting to Redis at redis://localhost:6379/
Deleting any existing JSON documents for RU204.
Dropping any existing search index.
Creating search index.
Loading JSON files from data/books.
Stored book In Real Life at key ru204:book:3721.
Stored book Lines of Departure at key ru204:book:729.
...
Lots more loading of books...
...
Stored book Good Omens: The Nice and Accurate Prophecies of Agnes Nutter, Witch at key ru204:book:28376.
Stored book Johannes Cabal and the Blustery Day: And Other Tales of the Necromancer at key ru204:book:35.
Stored book Eternity's Wheel at key ru204:book:182.
Stored book Shards and Ashes at key ru204:book:478.
Loaded 1486 books into Redis.
Data verification checks completed OK.
```

If you see the "Loaded 1486 books into Redis." and "Data verification checks completed OK." messages then you've completed the setup steps and are ready to go.

## You're Ready!

You're now ready to take the course!  If you haven't already, [sign up here](https://university.redis.com/courses/ru204/) to access the course materials.

## You're Not Alone!

If you need help or want to chat about all things Redis, [join us on our Discord server](https://discord.gg/46upnugY5B) where you'll find a dedicated channel `#ru204-storing-querying-and-indexing-json-at-speed` for this course.
