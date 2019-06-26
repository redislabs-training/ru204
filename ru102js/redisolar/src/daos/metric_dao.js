const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('metric');

const insert = meterReading => impl.insert(meterReading);

const getRecent = (siteId, unit, time, limit) => impl.getRecent(siteId, unit, time, limit);

module.exports = {
  insert,
  getRecent,
};
