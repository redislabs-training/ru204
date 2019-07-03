const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('ratelimiter');

const hit = async name => impl.hit(name);

module.exports = {
  hit,
};
