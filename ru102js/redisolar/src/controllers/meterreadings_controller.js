const metricDao = require('../daos/metric_dao');
const siteStatsDao = require('../daos/sitestats_dao');
const capacityDao = require('../daos/capacity_dao');
const feedDao = require('../daos/feed_dao');

const getLimit = (n) => {
  if (Number.isNaN(n)) {
    return 100;
  }

  return (n > 1000 ? 1000 : n);
};

const createMeterReadings = async (req, res, next) => {
  try {
    // TODO does order matter here, or are there
    // dependencies... if so a for loop with multiple
    // awaits might be better...
    await req.body.map(async (meterReading) => Promise.all([
        metricDao.insert(meterReading),
        siteStatsDao.update(meterReading),
        capacityDao.update(meterReading),
        feedDao.insert(meterReading),
      ])
    );

    return res.status(201).send('OK');
  } catch (err) {
    return next(err);
  }
};

const getMeterReadings = async (req, res, next) => {
  try {
    const readings = await feedDao.getRecentGlobal(getLimit(req.query.n));

    return res.status(200).json(readings);
  } catch (err) {
    return next(err);
  }
};

const getMeterReadingsForSite = async (req, res, next) => {
  try {
    const { siteId, n } = req.params;

    return res.status(200).json(feedDao.getRecentForSite(siteId, getLimit(n)));
  } catch (err) {
    return next(err);
  }
};

module.exports = {
  createMeterReadings,
  getMeterReadings,
  getMeterReadingsForSite,
};
