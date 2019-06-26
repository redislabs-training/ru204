const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('ratelimiter');

const hit = name => impl.hit(name);

module.exports = {
  hit,
};
