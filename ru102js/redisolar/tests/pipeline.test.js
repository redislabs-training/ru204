const redis = require('../src/daos/impl/redis/redis_client');

const client = redis.getClient();

const testSuiteName = 'pipeline';
const testKeyPrefix = `test:${testSuiteName}`;

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

test(`${testSuiteName}: example command pipeline`, async () => {
  const pipeline = client.batch();
  const testKey = `${testKeyPrefix}:example_pipeline`;

  pipeline.set(testKey, 1);
  pipeline.incr(testKey);
  pipeline.get(testKey);

  const replies = await pipeline.execAsync();

  expect(replies).toHaveLength(3);
  expect(replies[0]).toBe('OK');
  expect(replies[1]).toBe(2);
  expect(replies[2]).toBe('2');
});

test(`${testSuiteName}: example pipeline with bad command`, async () => {
  const pipeline = client.batch();
  const testKey = `${testKeyPrefix}:example_bad_pipeline`;

  pipeline.set(testKey, 1);
  pipeline.incr(testKey, 99); // Error, wrong number of arguments!
  pipeline.get(testKey);

  const replies = await pipeline.execAsync();

  expect(replies).toHaveLength(3);
  expect(replies[0]).toBe('OK');
  expect(replies[1]).toEqual({
    command: 'INCR',
    args: [
      testKey,
      99,
    ],
    code: 'ERR',
    position: 1,
  });
  expect(replies[2]).toBe('1');
});

/* eslint-enable */
