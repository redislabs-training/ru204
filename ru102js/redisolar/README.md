# RediSolar for Node.js

## TODO List

* Complete `LICENSE`
* Integrate Vue app (currently ships with built version - I'd like to just ship the built version TBH)
* Write some more tests
* Complete `README.md`
* Complete static DAOs
* JSDoc comments
* Tidy up field names into constants
* See if I need to implement the sliding window rate limiter solution or just offer this as a challenge to the students.  Probably should have a stock answer...
* See if I need to implement the optimized find by geo with capacity that uses intermediate stored results on the server (Itamar's suggestion) or just offer this as a challenge to the students.  Probably should have a stock answer...

# Introduction

This is the sample application codebase for RU102JS, Redis for JavaScript developers.

TODO.

# Prerequisites

In order to start and run this application, you will need:

* [Node.js](https://nodejs.org/en/download/) (8.9.4 or newer, we recommend using the current Long Term Stable version)
* npm (installed with Node.js)
* Access to a local or remote installation of [Redis](https://redis.io/download) version 5 or newer

# Setup

To get started with the default configuration (server on port 80, Redis on localhost port 6379):

```
$ npm install
$ npm run dev
```

This should start a live reloading server that uses [nodemon](https://www.npmjs.com/package/nodemon).  You should be able to see the front end solar dashboard app at: 

```
http://localhost:8080/
```

# Configuration 

TODO tour of `config.json`.

# Load Sample Data

To load sample site data and sample metrics, run:

```
npm run load src/resources/data/sites.json flushdb
```

`flushdb` is optional, and will erase ALL data from Redis before inserting the sample data.

# Development Workflow

TODO

```
npm run dev
```

Edit code, application will hot reload on save.

## Running Tests

The project is setup to use [Jest](https://jestjs.io/en/) for testing.  To run all tests:

```
npm test
```

To run a specific suite of tests (e.g. those in `tests/basic.test.js`):

```
npm test -t basic
```

To run Jest continuously in watch mode, which gives you access to menus allowing you to run 
subsets of tests and many more options:

```
npm testdev
```

## Linting

TODO description, info, `.eslintrc`, `.eslintignore`.

```
npm run lint
```
