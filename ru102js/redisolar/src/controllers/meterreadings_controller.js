const metricDao = require('../daos/metric_dao');
const siteStatsDao = require('../daos/sitestats_dao');
const capacityDao = require('../daos/capacity_dao');
const feedDao = require('../daos/feed_dao');

const createMeterReadings = async (meterReadings) => {
  for (const meterReading of meterReadings) {
    /* eslint-disable no-await-in-loop */
    await metricDao.insert(meterReading);
    await siteStatsDao.update(meterReading);
    await capacityDao.update(meterReading);
    await feedDao.insert(meterReading);
    /* eslint-enable */
  }
};

const getMeterReadings = async limit => feedDao.getRecentGlobal(limit);

const getMeterReadingsForSite = async (siteId, limit) => feedDao.getRecentForSite(siteId, limit);

module.exports = {
  createMeterReadings,
  getMeterReadings,
  getMeterReadingsForSite,
};
