const config = require('better-config');
const redis = require('../src/daos/impl/redis/redis_client');
const redisCapacityDAO = require('../src/daos/impl/redis/capacity_dao_redis_impl');
const keyGenerator = require('../src/daos/impl/redis/redis_key_generator');

const testSuiteName = 'site_dao_redis_impl';

const testKeyPrefix = 'test';

config.set('../config.json');
keyGenerator.setPrefix(testKeyPrefix);
const client = redis.getClient();

/* eslint-disable no-undef */

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

test.todo(`${testSuiteName}: write tests!`);

/* eslint-enable */
