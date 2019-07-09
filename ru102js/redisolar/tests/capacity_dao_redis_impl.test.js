const config = require('better-config');
const redis = require('../src/daos/impl/redis/redis_client');
const redisCapacityDAO = require('../src/daos/impl/redis/capacity_dao_redis_impl');
const keyGenerator = require('../src/daos/impl/redis/redis_key_generator');

const testSuiteName = 'capacity_dao_redis_impl';

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

test.todo(`${testSuiteName}: update`);

test.todo(`${testSuiteName}: getReport`);

test(`${testSuiteName}: getRank`, async () => {
  // Create some data
  const entries = [
    {
      id: 1,
      score: 10,
    },
    {
      id: 2,
      score: 15,
    },
    {
      id: 3,
      score: 30,
    },
    {
      id: 4,
      score: 20,
    },
    {
      id: 5,
      score: 50,
    },
  ];

  await Promise.all(
    entries.map(
      site => client.zaddAsync(
        keyGenerator.getCapacityRankingKey(),
        site.score,
        site.id,
      ),
    ),
  );

  let result = await redisCapacityDAO.getRank(1);
  expect(result).toBe(4);

  result = await redisCapacityDAO.getRank(2);
  expect(result).toBe(3);

  result = await redisCapacityDAO.getRank(3);
  expect(result).toBe(1);

  result = await redisCapacityDAO.getRank(4);
  expect(result).toBe(2);

  result = await redisCapacityDAO.getRank(5);
  expect(result).toBe(0);

  // Test invalid member.
  result = await redisCapacityDAO.getRank(6);
  expect(result).toBe(null);
});

/* eslint-enable */
