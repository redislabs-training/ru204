const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('feed');

const insert = meterReading => impl.insert(meterReading);

const getRecentGlobal = limit => impl.getRecentGlobal(limit);

const getRecentForSite = (siteId, limit) => impl.getRecentForSite(siteId, limit);

module.exports = {
  insert,
  getRecentGlobal,
  getRecentForSite,
};
