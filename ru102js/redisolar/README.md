# RediSolar for Node.js

## TODO List

* Complete `LICENSE`
* Integrate Vue app (currently ships with built version)
* Choose and install a test framework - likely [Jest](https://jestjs.io/en/)
* Fix double newline bug in winston when logging from morgan
* Do better with eslint than `npm run lint`
* Complete `README.md`
* Complete static DAOs
* Complete Redis DAOs
* JSDoc comments

# Introduction

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

# Development Workflow

TODO

## Linting

TODO

```
npm run lint
```
