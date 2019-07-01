const config = require('better-config');

config.set('../config.json');

const keyGenerator = require('../src/daos/impl/redis/redis_key_generator');

const testSuiteName = 'redis_key_generator';
const expectedKeyPrefix = 'test';

beforeAll(() => {
  keyGenerator.setPrefix(expectedKeyPrefix);
});

/* eslint-disable no-undef */

test(`${testSuiteName}:getSiteHashId`, () => {
  expect(keyGenerator.getSiteHashKey(999)).toBe(`${expectedKeyPrefix}:sites:info:999`);
});

test(`${testSuiteName}:getSiteIDsKey`, () => {
  expect(keyGenerator.getSiteIDsKey()).toBe(`${expectedKeyPrefix}:sites:ids`);
});

test.todo(`${testSuiteName}:getSiteStatsKey`);

test(`${testSuiteName}:getRateLimiterKey`, () => {
  expect(keyGenerator.getRateLimiterKey('test', 1, 12)).toBe(`${expectedKeyPrefix}:test:1:12`);
});

test(`${testSuiteName}:getSiteGeoKey`, () => {
  expect(keyGenerator.getSiteGeoKey()).toBe(`${expectedKeyPrefix}:sites:geo`);
});

test(`${testSuiteName}:getCapacityRankingKey`, () => {
  expect(keyGenerator.getCapacityRankingKey()).toBe(`${expectedKeyPrefix}:sites:capacity:ranking`);
});

test(`${testSuiteName}:getTSKey`, () => {
  expect(keyGenerator.getTSKey(99, 'test')).toBe(`${expectedKeyPrefix}:sites:ts:99:test`);
});

test.todo(`${testSuiteName}:getDayMetricKey`);

test(`${testSuiteName}:getGlobalFeedKey`, () => {
  expect(keyGenerator.getGlobalFeedKey()).toBe(`${expectedKeyPrefix}:sites:feed`);
});

test(`${testSuiteName}:getFeedKey`, () => {
  expect(keyGenerator.getFeedKey(99)).toBe(`${expectedKeyPrefix}:sites:feed:99`);
});

test(`${testSuiteName}:setPrefix`, () => {
  expect(keyGenerator.getSiteIDsKey()).toBe(`test:sites:ids`);
});

/* eslint-enable */
