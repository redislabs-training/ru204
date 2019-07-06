const metricDao = require('../daos/metric_dao');

const getMetricsForSite = async (req, res, next) => {
  try {
    const { siteId, n } = req.params;
    const limit = Number.isNaN(n) ? 120 : n;
    const currentTimestamp = new Date().getTime();

    // Get both things in parallel with a promise all...
    const metrics = await Promise.all([
      metricDao.getRecent(siteId, 'generated unit', currentTimestamp, limit),
      metricDao.getRecent(siteId, 'used unit', currentTimestamp, limit),
    ]);

    return res.status(200).json([{
      measurements: metrics[0],
      name: 'Watt-Hours Generated',
    }, {
      measurements: metrics[1],
      name: 'Watt-Hours Used',
    }]);
  } catch (err) {
    return next(err);
  }
};

module.exports = {
  getMetricsForSite,
};
