const redis = require('./redis_client');
const keyGenerator = require('./redis_key_generator');

/**
 *
 * @param {string} name - TODO
 * @param {Object} opts - TODO
 * @returns {Promise} - TODO
 * @private
 */
const hitFixedWindow = async (name, opts) => {
  const client = redis.getClient();
  const key = keyGenerator.getRateLimiterKey(name, opts.interval, opts.maxHits);

  const pipeline = client.batch();

  pipeline.incr(key);
  pipeline.expire(key, opts.interval * 60);

  const response = await pipeline.execAsync();
  const hits = parseInt(response[0], 10);

  return Math.max(0, opts.maxHits - hits);
};

/* eslint-disable no-unused-vars */
const hitSlidingWindow = async (name, opts) => {
  // TODO implement hitSlidingWindow...
};
/* eslint-enable */

/**
 * Record a hit against a unique resource that is being
 * rate limited.  Will return 0 when the resource has hit
 * the rate limit.
 * @param {string} name - the unique name of the resource.
 * @param {Object} opts - object containing maxHits and interval details.
 * @returns {Promise} - Promise that resolves to number of hits remaining.
 */
const hit = async (name, opts) => hitFixedWindow(name, opts);

module.exports = {
  hit,
};
