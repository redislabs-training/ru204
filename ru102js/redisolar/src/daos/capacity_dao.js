const daoLoader = require('./daoloader');

const impl = daoLoader.loadDao('capacity');

const update = async meterReading => impl.update(meterReading);

const getReport = async limit => impl.getReport(limit);

const getRank = async siteId => impl.getRank(siteId);

module.exports = {
  update,
  getReport,
  getRank,
};
