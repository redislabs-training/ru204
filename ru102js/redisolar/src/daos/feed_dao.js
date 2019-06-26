const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('feed');

const insert = meterReadings => impl.insert(meterReadings);

const getRecentGlobal = limit => impl.getRecentGlobal(limit);

const getRecentForSite = (siteId, limit) => impl.getRecentForSite(siteId, limit);

module.exports = {
  insert,
  getRecentGlobal,
  getRecentForSite,
};
