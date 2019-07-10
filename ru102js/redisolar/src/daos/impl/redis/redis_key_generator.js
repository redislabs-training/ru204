const moment = require('moment');
const config = require('better-config');

let prefix = config.get('dataStores.redis.keyPrefix');

const getKey = key => `${prefix}:${key}`;

const formatTimestamp = timestamp => moment.unix(timestamp).utc().format('YYYY-MM-DD');

const getSiteHashKey = siteId => getKey(`sites:info:${siteId}`);

const getSiteIDsKey = () => getKey('sites:ids');

const getSiteStatsKey = (siteId, timestamp) => 'TODO';

const getRateLimiterKey = (name, minute, maxHits) => getKey(`${name}:${minute}:${maxHits}`);

const getSiteGeoKey = () => getKey('sites:geo');

const getCapacityRankingKey = () => getKey('sites:capacity:ranking');

const getTSKey = (siteId, unit) => getKey(`sites:ts:${siteId}:${unit}`);

const getDayMetricKey = (siteId, unit, timestamp) => getKey(
  `metric:${unit}:${formatTimestamp(timestamp)}:${siteId}`,
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
