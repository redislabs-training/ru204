const config = require('better-config');
const redis = require('../src/daos/impl/redis/redis_client');
const redisRateLimiterDAO = require('../src/daos/impl/redis/sliding_ratelimiter_dao_redis_impl');
const keyGenerator = require('../src/daos/impl/redis/redis_key_generator');

const testSuiteName = 'ratelimiter_dao_redis_impl';

const testKeyPrefix = `test:${testSuiteName}`;

config.set('../config.json');
keyGenerator.setPrefix(testKeyPrefix);
const client = redis.getClient();

/* eslint-disable no-undef, no-await-in-loop */

beforeAll(() => {
  jest.setTimeout(60000);
});

afterEach(async () => {
  const testKeys = await client.keysAsync(`${testKeyPrefix}:*`);

  if (testKeys.length > 0) {
    await client.delAsync(testKeys);
  }
});

afterAll(() => {
  // Release Redis connection.
  client.quit();
});

// Challenge 7. TODO THIS SHOULD BE SKIPPED INITIALLY
test(`${testSuiteName}: hit (sliding window limit not exceeded)`, async () => {
  const limiterOpts = {
    interval: 10000,
    maxHits: 5,
  };

  let remains = await redisRateLimiterDAO.hit('testresource', limiterOpts);
  console.log(remains);
  remains = await redisRateLimiterDAO.hit('testresource', limiterOpts);
  console.log(remains);
  remains = await redisRateLimiterDAO.hit('testresource', limiterOpts);
  console.log(remains);
  remains = await redisRateLimiterDAO.hit('testresource', limiterOpts);
  console.log(remains);
  remains = await redisRateLimiterDAO.hit('testresource', limiterOpts);
  console.log(remains);
  remains = await redisRateLimiterDAO.hit('testresource', limiterOpts);
  console.log(remains);
});

// Challenge 7. TODO THIS SHOULD BE SKIPPED INITIALLY
test.todo(`${testSuiteName}: hit (sliding window limit exceeded)`);

/* eslint-enable */
