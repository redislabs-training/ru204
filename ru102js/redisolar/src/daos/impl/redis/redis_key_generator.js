const config = require('better-config');
const timeUtils = require('../../../utils/time_utils');

// Prefix that all keys will start with, taken from config.json
let prefix = config.get('dataStores.redis.keyPrefix');

const getKey = key => `${prefix}:${key}`;

// sites:info:[siteId]
// Redis type: hash
const getSiteHashKey = siteId => getKey(`sites:info:${siteId}`);

// sites:ids
// Redis type: set
const getSiteIDsKey = () => getKey('sites:ids');

// sites:stats:[year-month-day]:[siteId]
// Redis type: sorted set
const getSiteStatsKey = (siteId, timestamp) => getKey(`sites:stats:${timeUtils.getDateString(timestamp)}:${siteId}`);

const getRateLimiterKey = (name, interval, maxHits) => {
  const minuteOfDay = timeUtils.getMinuteOfDay();
  return getKey(`limiter:${name}:${Math.floor(minuteOfDay / interval)}:${maxHits}`);
};

// sites:geo
// Redis type: geo
const getSiteGeoKey = () => getKey('sites:geo');

// sites:capacity:ranking
// Redis type: sorted set
const getCapacityRankingKey = () => getKey('sites:capacity:ranking');

// sites:ts:[siteId]:[unit]
// Redis type: RedisTimeSeries
const getTSKey = (siteId, unit) => getKey(`sites:ts:${siteId}:${unit}`);

// metric:[unit][year-month-day]:[siteId]
// Redis type: sorted set
const getDayMetricKey = (siteId, unit, timestamp) => getKey(
  `metric:${unit}:${timeUtils.getDateString(timestamp)}:${siteId}`,
);

// sites:feed
// Redis type: stream
const getGlobalFeedKey = () => getKey('sites:feed');

// sites:feed:[siteId]
// Redis type: stream
const getFeedKey = siteId => getKey(`sites:feed:${siteId}`);

const setPrefix = (newPrefix) => {
  prefix = newPrefix;
};

module.exports = {
  getSiteHashKey,
  getSiteIDsKey,
  getSiteStatsKey,
  getRateLimiterKey,
  getSiteGeoKey,
  getCapacityRankingKey,
  getTSKey,
  getDayMetricKey,
  getGlobalFeedKey,
  getFeedKey,
  setPrefix,
};
