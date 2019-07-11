const redis = require('./redis_client');
const keyGenerator = require('./redis_key_generator');

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

const hit = async (name, opts) => hitFixedWindow(name, opts);

module.exports = {
  hit,
};
