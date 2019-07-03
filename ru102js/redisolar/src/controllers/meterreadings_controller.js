const logger = require('../utils/logger');
const feedDao = require('../daos/feed_dao');

const createMeterReading = async (req, res, next) => {
  try {
    return res.status(200).json(feedDao.insert(req.body));
  } catch (err) {
    return next(err);
  }
};

const getMeterReadings = async (req, res, next) => {
  try {
    const limit = Number.isNaN(req.query.n) ? undefined : req.query.n;

    if (limit) {
      logger.debug(`Limit is ${limit}.`);
    }

    const readings = await feedDao.getRecentGlobal(limit);

    return res.status(200).json(readings);
  } catch (err) {
    return next(err);
  }
};

const getMeterReadingsForSite = async (req, res, next) => {
  try {
    const { siteId } = req.params;
    const limit = Number.isNaN(req.query.n) ? undefined : req.query.n;

    if (limit) {
      logger.debug(`Limit is ${limit}.`);
    }

    return res.status(200).json(feedDao.getRecentForSite(siteId, limit));
  } catch (err) {
    next(err);
  }
};

module.exports = {
  createMeterReading,
  getMeterReadings,
  getMeterReadingsForSite,
};
