const logger = require('../utils/logger');
const feedDao = require('../daos/feed_dao');

const createMeterReading = (req, res) => res.status(200).json(feedDao.insert(req.body));

const getMeterReadings = (req, res) => {
  const limit = req.query.n;
  logger.debug(`Limit is ${limit}.`);

  return res.status(200).json(feedDao.getRecentGlobal(limit));
};

const getMeterReadingsForSite = (req, res) => {
  const { siteId } = req.params;
  const limit = req.query.n;

  logger.debug(`Limit is ${limit}.`);

  return res.status(200).json(feedDao.getRecentForSite(siteId, limit));
};

module.exports = {
  createMeterReading,
  getMeterReadings,
  getMeterReadingsForSite,
};
