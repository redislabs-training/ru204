const config = require('better-config');
const redis = require('../src/daos/impl/redis/redis_client');
const keyGenerator = require('../src/daos/impl/redis/redis_key_generator');

const testSuiteName = 'metrics_controller';

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

test.todo(`${testSuiteName}: getMetricsForSite`);

/* eslint-enable */
