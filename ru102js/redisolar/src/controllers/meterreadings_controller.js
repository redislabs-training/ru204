const metricDao = require('../daos/metric_dao');
const siteStatsDao = require('../daos/sitestats_dao');
const capacityDao = require('../daos/capacity_dao');
const feedDao = require('../daos/feed_dao');

const createMeterReadings = async (meterReadings) => {
  // TODO does order matter here, or are there
  // dependencies... if so a for loop with multiple
  // awaits might be better...
  await meterReadings.map(async meterReading => Promise.all([
    metricDao.insert(meterReading),
    siteStatsDao.update(meterReading),
    capacityDao.update(meterReading),
    feedDao.insert(meterReading),
  ]));
};

const getMeterReadings = async limit => feedDao.getRecentGlobal(limit);

const getMeterReadingsForSite = async (siteId, limit) => feedDao.getRecentForSite(siteId, limit);

module.exports = {
  createMeterReadings,
  getMeterReadings,
  getMeterReadingsForSite,
};
