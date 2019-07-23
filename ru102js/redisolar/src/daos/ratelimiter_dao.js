const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('ratelimiter');

/**
 * Record a hit against a unique resource that is being 
 * rate limited.  Will return 0 when the resource has hit 
 * the rate limit.
 * @param {string} name - the unique name of the resource.
 * @param {Object} opts - object containing maxHits and interval details.
 * @returns {Promise} - Promise that resolves to number of hits remaining.
 */
const hit = async (name, opts) => impl.hit(name, opts);

module.exports = {
  hit,
};
