const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('capacity');

const update = meterReading => impl.update(meterReading);

const getReport = limit => impl.getReport(limit);

const getRank = siteId => impl.getRank(siteId);

module.exports = {
  update,
  getReport,
  getRank,
};
