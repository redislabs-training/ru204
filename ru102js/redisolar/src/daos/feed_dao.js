const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('feed');

const insert = async meterReadings => impl.insert(meterReadings);

const getRecentGlobal = async limit => impl.getRecentGlobal(limit);

const getRecentForSite = async (siteId, limit) => impl.getRecentForSite(siteId, limit);

module.exports = {
  insert,
  getRecentGlobal,
  getRecentForSite,
};
