const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('metric');

const insert = async meterReading => impl.insert(meterReading);

const getRecent = async (siteId, unit, time, limit) => impl.getRecent(siteId, unit, time, limit);

module.exports = {
  insert,
  getRecent,
};
