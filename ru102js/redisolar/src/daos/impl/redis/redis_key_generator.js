const config = require('better-config');

const getKey = key => `${config.get('dataStores.redis.keyPrefix')}:${key}`;

const getSiteHashKey = siteId => getKey(`sites:info:${siteId}`);

const getSiteIDsKey = () => getKey('sites:ids');

const getSiteStatsKey = (siteId, timestamp) => 'TODO';

const getRateLimiterKey = (name, minute, maxHits) => getKey(`${name}:${minute}:${maxHits}`);

const getSiteGeoKey = () => getKey('sites:geo');

const getCapacityRankingKey = () => getKey('sites:capacity:ranking');

const getTSKey = (siteId, unit) => getKey(`sites:ts:${siteId}:${unit}`);

const getDayMetricKey = (siteId, unit, timestamp) => 'TODO';

const getGlobalFeedKey = () => getKey('sites:feed');

const getFeedKey = siteId => getKey(`sites:feed:${siteId}`);

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
};
