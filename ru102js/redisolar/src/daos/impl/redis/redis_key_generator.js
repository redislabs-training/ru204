const config = require('better-config');
const timeUtils = require('../../../utils/time_utils');

let prefix = config.get('dataStores.redis.keyPrefix');

const getKey = key => `${prefix}:${key}`;

const getSiteHashKey = siteId => getKey(`sites:info:${siteId}`);

const getSiteIDsKey = () => getKey('sites:ids');

const getSiteStatsKey = (siteId, timestamp) => getKey(`sites:stats:${timeUtils.getDateString(timestamp)}:${siteId}`);

const getRateLimiterKey = (name, interval, maxHits) => {
  const minuteOfDay = timeUtils.getMinuteOfDay();
  return getKey(`limiter:${name}:${Math.floor(minuteOfDay / interval)}:${maxHits}`);
};

const getSiteGeoKey = () => getKey('sites:geo');

const getCapacityRankingKey = () => getKey('sites:capacity:ranking');

const getTSKey = (siteId, unit) => getKey(`sites:ts:${siteId}:${unit}`);

const getDayMetricKey = (siteId, unit, timestamp) => getKey(
  `metric:${unit}:${timeUtils.getDateString(timestamp)}:${siteId}`,
);

const getGlobalFeedKey = () => getKey('sites:feed');

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
