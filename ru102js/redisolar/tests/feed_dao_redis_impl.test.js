const config = require('better-config');
const redis = require('../src/daos/impl/redis/redis_client');
const redisFeedDAO = require('../src/daos/impl/redis/feed_dao_redis_impl');
const keyGenerator = require('../src/daos/impl/redis/redis_key_generator');

const testSuiteName = 'feed_dao_redis_impl';

const testKeyPrefix = 'test';

config.set('../config.json');
keyGenerator.setPrefix(testKeyPrefix);
const client = redis.getClient();

const testSiteId = 999;

const generateMeterReading = () => ({
  siteId: testSiteId,
  dateTime: new Date().getTime(),
  tempC: 22,
  whUsed: 1.2,
  whGenerated: 1.4,
});

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

test(`${testSuiteName}: insert and read back from global stream`, async () => {
  const testMeterReading1 = generateMeterReading();
  const testMeterReading2 = generateMeterReading();

  await redisFeedDAO.insert(testMeterReading1);
  await redisFeedDAO.insert(testMeterReading2);

  // Test global feed with and without limit.
  let meterReadings = await redisFeedDAO.getRecentGlobal(100);

  // TODO compare readings...

  expect(meterReadings.length).toBe(2);

  meterReadings = await redisFeedDAO.getRecentGlobal(1);
  expect(meterReadings.length).toBe(1);
});

test(`${testSuiteName}: read stream for site that does not exist`, async () => {
  const meterReadings = await redisFeedDAO.getRecentForSite(-1, 100);

  expect(meterReadings.length).toBe(0);
});

test(`${testSuiteName}: insert and read back from site specific stream`, async () => {
  const testMeterReading1 = generateMeterReading();
  const testMeterReading2 = generateMeterReading();

  await redisFeedDAO.insert(testMeterReading1);
  await redisFeedDAO.insert(testMeterReading2);

  // Test global feed with and without limit.
  let meterReadings = await redisFeedDAO.getRecentForSite(testSiteId, 100);

  // TODO compare readings...

  expect(meterReadings.length).toBe(2);

  meterReadings.map(meterReading => expect(meterReading.siteId).toBe(testSiteId));

  meterReadings = await redisFeedDAO.getRecentForSite(testSiteId, 1);
  expect(meterReadings.length).toBe(1);
});

test.todo(`${testSuiteName}: test body of meter readings for expected values`);

/* eslint-enable */
