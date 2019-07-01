const config = require('better-config');
const keyGenerator = require('../src/daos/impl/redis/redis_key_generator');

config.set('../config.json');

const expectedKeyPrefix = config.get('dataStores.redis.keyPrefix');

/* eslint-disable no-undef */

test('Key Generator:getSiteHashId', () => {
  expect(keyGenerator.getSiteHashKey(999)).toBe(`${expectedKeyPrefix}:sites:info:999`);
});

test('Key Generator:getSiteIDsKey', () => {
  expect(keyGenerator.getSiteIDsKey()).toBe(`${expectedKeyPrefix}:sites:ids`);
});

test('Key Generator:getSiteStatsKey', () => {
  expect(keyGenerator.getSiteStatsKey()).toBe('TODO'); // TODO real test...
});

test('Key Generator:getRateLimiterKey', () => {
  expect(keyGenerator.getRateLimiterKey('test', 1, 12)).toBe(`${expectedKeyPrefix}:test:1:12`);
});

test('Key Generator:getSiteGeoKey', () => {
  expect(keyGenerator.getSiteGeoKey()).toBe(`${expectedKeyPrefix}:sites:geo`);
});

test('Key Generator:getCapacityRankingKey', () => {
  expect(keyGenerator.getCapacityRankingKey()).toBe(`${expectedKeyPrefix}:sites:capacity:ranking`);
});

test('Key Generator:getTSKey', () => {
  expect(keyGenerator.getTSKey(99, 'test')).toBe(`${expectedKeyPrefix}:sites:ts:99:test`);
});

test('Key Generator:getDayMetricKey', () => {
  expect(keyGenerator.getDayMetricKey(99, 'TODO', 0)).toBe('TODO'); // TODO real test...
});

test('Key Generator:getGlobalFeedKey', () => {
  expect(keyGenerator.getGlobalFeedKey()).toBe(`${expectedKeyPrefix}:sites:feed`);
});

test('Key Generator:getFeedKey', () => {
  expect(keyGenerator.getFeedKey(99)).toBe(`${expectedKeyPrefix}:sites:feed:99`);
});

/* eslint-enable */
