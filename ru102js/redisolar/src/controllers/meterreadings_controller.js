const feedDao = require('../daos/feed_dao');

const getLimit = (n) => {
  if (Number.isNaN(n)) {
    return 100;
  }

  return (n > 1000 ? 1000 : n);
};

const createMeterReading = async (req, res, next) => {
  try {
    return res.status(200).json(feedDao.insert(req.body));
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
  createMeterReading,
  getMeterReadings,
  getMeterReadingsForSite,
};
