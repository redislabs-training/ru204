# RediSolar for Node.js

## TODO List

* Complete `LICENSE`
* Integrate Vue app (currently ships with built version)
* Choose and install a test framework - likely Jest
* Fix double newline bug in winston when logging from morgan
* Do better with eslint than `npm run lint`
* Complete `README.md`
* Complete static DAOs
* Complete Redis DAOs

# Introduction

TODO.

# Prerequisites

In order to start and run this application, you will need:

* [Node.js](https://nodejs.org/en/download/) (8.9.4 or newer, we recommend using the current Long Term Stable version)
* npm (installed with Node.js)
* Access to a local or remote installation of [Redis](https://redis.io/download) version 5 or newer

# Setup

To get started:

```
$ npm install
$ npm run dev
```

This should start a live reloading server that uses [nodemon](https://www.npmjs.com/package/nodemon).  You should be able to see the front end solar dashboard app at: 

```
http://localhost:8080/
```
