const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('metric');

const insert = async meterReading => impl.insert(meterReading);

const getRecent = async (siteId, metricUnit, timestamp, limit) => impl.getRecent(
  siteId,
  metricUnit,
  timestamp,
  limit,
);

module.exports = {
  insert,
  getRecent,
};
